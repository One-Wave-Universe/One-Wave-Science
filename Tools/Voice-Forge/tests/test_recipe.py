from engine.recipe import Recipe, SourceEntry


def test_recipe_roundtrip(tmp_path):
    recipe = Recipe.default_two_source("a.wav", "b.wav", name="Test Voice")
    recipe.traits.pitch_semitones = -3.5
    recipe.traits.formant_ratio = 1.15
    recipe.finishing.reverb.enabled = True
    recipe.finishing.reverb.mix = 0.4
    recipe.locked_traits = ["pitch_semitones"]

    path = str(tmp_path / "voice.recipe.json")
    recipe.save(path)
    reloaded = Recipe.load(path)

    assert reloaded.name == "Test Voice"
    assert len(reloaded.sources) == 2
    assert reloaded.sources[0].id == "A"
    assert reloaded.traits.pitch_semitones == -3.5
    assert reloaded.traits.formant_ratio == 1.15
    assert reloaded.finishing.reverb.enabled is True
    assert reloaded.finishing.reverb.mix == 0.4
    assert reloaded.locked_traits == ["pitch_semitones"]


def test_recipe_clone_is_independent():
    recipe = Recipe.default_two_source("a.wav", "b.wav")
    clone = recipe.clone()
    clone.traits.pitch_semitones = 5.0
    clone.sources[0].amount = 0.9

    assert recipe.traits.pitch_semitones == 0.0
    assert recipe.sources[0].amount == 0.5


def test_source_entry_defaults():
    entry = SourceEntry(id="C", path="c.wav")
    assert entry.amount == 1.0
    assert entry.mute is False
    assert entry.solo is False
