//! Cells worker: deterministic parsing primitives only.
//!
//! Contract:
//! - Input: raw Director text.
//! - Output: a typed `CellIntent`.
//! - No routing, project mutation, creative planning, or execution happens here.

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CellIntent {
    Play,
    Stop,
    AddFrame,
    DuplicateFrame,
    DeleteFrame,
    Undo,
    SelectFrame { frame: u32 },
    SetFps { fps: u32 },
    SetHold { hold: u32 },
    SceneRequest { text: String },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CellError {
    EmptyInput,
    ZeroNotAllowed { field: &'static str },
}

#[derive(Debug, Default, Clone, Copy)]
pub struct Cells;

impl Cells {
    pub fn parse(&self, raw: &str) -> Result<CellIntent, CellError> {
        let text = normalize_space(raw);
        if text.is_empty() {
            return Err(CellError::EmptyInput);
        }

        let lower = text.to_ascii_lowercase();

        match lower.as_str() {
            "play" | "play it" | "preview" => return Ok(CellIntent::Play),
            "stop" | "stop it" | "stop playback" => return Ok(CellIntent::Stop),
            "add frame" | "add a frame" | "new frame" => return Ok(CellIntent::AddFrame),
            "duplicate" | "duplicate frame" | "copy frame" => return Ok(CellIntent::DuplicateFrame),
            "delete frame" | "delete this frame" | "remove frame" => return Ok(CellIntent::DeleteFrame),
            "undo" | "undo that" | "go back" => return Ok(CellIntent::Undo),
            _ => {}
        }

        if let Some(value) = parse_prefixed_u32(&lower, &["go to frame", "select frame", "frame"]) {
            return Ok(CellIntent::SelectFrame { frame: nonzero("frame", value)? });
        }

        if let Some(value) = parse_prefixed_u32(&lower, &["set fps to", "set fps", "fps"]) {
            return Ok(CellIntent::SetFps { fps: nonzero("fps", value)? });
        }

        if let Some(value) = parse_prefixed_u32(&lower, &["set hold to", "set hold", "hold"]) {
            return Ok(CellIntent::SetHold { hold: nonzero("hold", value)? });
        }

        Ok(CellIntent::SceneRequest { text })
    }
}

fn normalize_space(raw: &str) -> String {
    raw.split_whitespace().collect::<Vec<_>>().join(" ")
}

fn nonzero(field: &'static str, value: u32) -> Result<u32, CellError> {
    if value == 0 {
        Err(CellError::ZeroNotAllowed { field })
    } else {
        Ok(value)
    }
}

fn parse_prefixed_u32(lower: &str, prefixes: &[&str]) -> Option<u32> {
    for prefix in prefixes {
        let Some(rest) = lower.strip_prefix(prefix) else { continue };
        let rest = rest.trim();
        if rest.is_empty() {
            continue;
        }
        let boundary_ok = lower
            .as_bytes()
            .get(prefix.len())
            .map(|b| b.is_ascii_whitespace())
            .unwrap_or(false);
        if boundary_ok && rest.chars().all(|c| c.is_ascii_digit()) {
            if let Ok(value) = rest.parse::<u32>() {
                return Some(value);
            }
        }
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rejects_empty_input() {
        assert_eq!(Cells.parse("   \n\t "), Err(CellError::EmptyInput));
    }

    #[test]
    fn normalizes_whitespace_but_preserves_scene_text_case() {
        assert_eq!(
            Cells.parse("  Make   GR   Run  "),
            Ok(CellIntent::SceneRequest { text: "Make GR Run".into() })
        );
    }

    #[test]
    fn parses_transport_primitives() {
        assert_eq!(Cells.parse("play"), Ok(CellIntent::Play));
        assert_eq!(Cells.parse("PREVIEW"), Ok(CellIntent::Play));
        assert_eq!(Cells.parse("stop playback"), Ok(CellIntent::Stop));
        assert_eq!(Cells.parse("undo that"), Ok(CellIntent::Undo));
    }

    #[test]
    fn parses_frame_primitives() {
        assert_eq!(Cells.parse("add frame"), Ok(CellIntent::AddFrame));
        assert_eq!(Cells.parse("duplicate frame"), Ok(CellIntent::DuplicateFrame));
        assert_eq!(Cells.parse("delete frame"), Ok(CellIntent::DeleteFrame));
        assert_eq!(Cells.parse("go to frame 12"), Ok(CellIntent::SelectFrame { frame: 12 }));
    }

    #[test]
    fn parses_timing_without_stealing_administrator_policy() {
        assert_eq!(Cells.parse("fps 24"), Ok(CellIntent::SetFps { fps: 24 }));
        assert_eq!(Cells.parse("set fps to 120"), Ok(CellIntent::SetFps { fps: 120 }));
        assert_eq!(Cells.parse("hold 6"), Ok(CellIntent::SetHold { hold: 6 }));
    }

    #[test]
    fn rejects_zero_positive_values() {
        assert_eq!(Cells.parse("frame 0"), Err(CellError::ZeroNotAllowed { field: "frame" }));
        assert_eq!(Cells.parse("fps 0"), Err(CellError::ZeroNotAllowed { field: "fps" }));
        assert_eq!(Cells.parse("hold 0"), Err(CellError::ZeroNotAllowed { field: "hold" }));
    }

    #[test]
    fn passes_open_ended_work_up_the_stack() {
        assert_eq!(
            Cells.parse("have GR run from left to right and kick the can"),
            Ok(CellIntent::SceneRequest {
                text: "have GR run from left to right and kick the can".into()
            })
        );
    }

    #[test]
    fn does_not_match_inside_another_word() {
        assert_eq!(
            Cells.parse("fpsboost 12"),
            Ok(CellIntent::SceneRequest { text: "fpsboost 12".into() })
        );
    }
}
