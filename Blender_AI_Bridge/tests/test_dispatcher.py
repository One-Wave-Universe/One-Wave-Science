import dispatcher


def setup_function(_fn):
    dispatcher._REGISTRY.clear()


def test_register_and_execute_command():
    @dispatcher.register("ping")
    def ping(value=1):
        return {"pong": value}

    result = dispatcher.execute_command("ping", {"value": 5})
    assert result == {"ok": True, "command": "ping", "result": {"pong": 5}, "error": None}


def test_execute_unknown_command():
    result = dispatcher.execute_command("does_not_exist")
    assert result["ok"] is False
    assert "unknown command" in result["error"]


def test_command_error_is_reported_not_raised():
    @dispatcher.register("boom")
    def boom():
        raise dispatcher.CommandError("bad params")

    result = dispatcher.execute_command("boom")
    assert result == {"ok": False, "command": "boom", "result": None, "error": "bad params"}


def test_duplicate_registration_raises():
    @dispatcher.register("dup")
    def dup():
        return None

    try:
        dispatcher.register("dup")(lambda: None)
        assert False, "expected RuntimeError"
    except RuntimeError:
        pass


def test_execute_commands_batch_continues_after_error_by_default():
    @dispatcher.register("ok_cmd")
    def ok_cmd():
        return "fine"

    @dispatcher.register("bad_cmd")
    def bad_cmd():
        raise dispatcher.CommandError("nope")

    results = dispatcher.execute_commands(
        [{"command": "bad_cmd"}, {"command": "ok_cmd"}]
    )
    assert [r["ok"] for r in results] == [False, True]


def test_execute_commands_stop_on_error():
    @dispatcher.register("bad_cmd")
    def bad_cmd():
        raise dispatcher.CommandError("nope")

    @dispatcher.register("never_runs")
    def never_runs():
        raise AssertionError("should not be called")

    results = dispatcher.execute_commands(
        [{"command": "bad_cmd"}, {"command": "never_runs"}], stop_on_error=True
    )
    assert len(results) == 1
    assert results[0]["ok"] is False


def test_describe_commands_lists_params():
    @dispatcher.register("greet")
    def greet(name, loud=False):
        """Say hello."""
        return name

    described = dispatcher.describe_commands()
    assert described["greet"]["summary"] == "Say hello."
    param_names = [p["name"] for p in described["greet"]["params"]]
    assert param_names == ["name", "loud"]
