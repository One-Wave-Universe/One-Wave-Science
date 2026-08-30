//! Micro Parser worker: deterministic parsing primitives only.
//!
//! Contract:
//! - Input: raw Director text.
//! - Output: a typed `ParserIntent`.
//! - No routing, project mutation, creative planning, or execution happens here.

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ParserIntent {
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
pub enum ParserError {
    EmptyInput,
    ZeroNotAllowed { field: &'static str },
}

#[derive(Debug, Default, Clone, Copy)]
pub struct Parser;

impl Parser {
    pub fn parse(&self, raw: &str) -> Result<ParserIntent, ParserError> {
        let text = normalize_space(raw);
        if text.is_empty() { return Err(ParserError::EmptyInput); }
        let lower = text.to_ascii_lowercase();
        match lower.as_str() {
            "play" | "play it" | "preview" => return Ok(ParserIntent::Play),
            "stop" | "stop it" | "stop playback" => return Ok(ParserIntent::Stop),
            "add frame" | "add a frame" | "new frame" => return Ok(ParserIntent::AddFrame),
            "duplicate" | "duplicate frame" | "copy frame" => return Ok(ParserIntent::DuplicateFrame),
            "delete frame" | "delete this frame" | "remove frame" => return Ok(ParserIntent::DeleteFrame),
            "undo" | "undo that" | "go back" => return Ok(ParserIntent::Undo),
            _ => {}
        }
        if let Some(value) = parse_prefixed_u32(&lower, &["go to frame", "select frame", "frame"]) {
            return Ok(ParserIntent::SelectFrame { frame: nonzero("frame", value)? });
        }
        if let Some(value) = parse_prefixed_u32(&lower, &["set fps to", "set fps", "fps"]) {
            return Ok(ParserIntent::SetFps { fps: nonzero("fps", value)? });
        }
        if let Some(value) = parse_prefixed_u32(&lower, &["set hold to", "set hold", "hold"]) {
            return Ok(ParserIntent::SetHold { hold: nonzero("hold", value)? });
        }
        Ok(ParserIntent::SceneRequest { text })
    }
}

fn normalize_space(raw: &str) -> String { raw.split_whitespace().collect::<Vec<_>>().join(" ") }

fn nonzero(field: &'static str, value: u32) -> Result<u32, ParserError> {
    if value == 0 { Err(ParserError::ZeroNotAllowed { field }) } else { Ok(value) }
}

fn parse_prefixed_u32(lower: &str, prefixes: &[&str]) -> Option<u32> {
    for prefix in prefixes {
        let Some(rest) = lower.strip_prefix(prefix) else { continue };
        let rest = rest.trim();
        if rest.is_empty() { continue; }
        let boundary_ok = lower.as_bytes().get(prefix.len()).map(|b| b.is_ascii_whitespace()).unwrap_or(false);
        if boundary_ok && rest.chars().all(|c| c.is_ascii_digit()) {
            if let Ok(value) = rest.parse::<u32>() { return Some(value); }
        }
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rejects_empty_input() { assert_eq!(Parser.parse("   \n\t "), Err(ParserError::EmptyInput)); }

    #[test]
    fn normalizes_whitespace_but_preserves_scene_text_case() {
        assert_eq!(Parser.parse("  Make   GR   Run  "), Ok(ParserIntent::SceneRequest { text: "Make GR Run".into() }));
    }

    #[test]
    fn parses_transport_primitives() {
        assert_eq!(Parser.parse("play"), Ok(ParserIntent::Play));
        assert_eq!(Parser.parse("PREVIEW"), Ok(ParserIntent::Play));
        assert_eq!(Parser.parse("stop playback"), Ok(ParserIntent::Stop));
        assert_eq!(Parser.parse("undo that"), Ok(ParserIntent::Undo));
    }

    #[test]
    fn parses_frame_primitives() {
        assert_eq!(Parser.parse("add frame"), Ok(ParserIntent::AddFrame));
        assert_eq!(Parser.parse("duplicate frame"), Ok(ParserIntent::DuplicateFrame));
        assert_eq!(Parser.parse("delete frame"), Ok(ParserIntent::DeleteFrame));
        assert_eq!(Parser.parse("go to frame 12"), Ok(ParserIntent::SelectFrame { frame: 12 }));
    }

    #[test]
    fn parses_timing_without_stealing_administrator_policy() {
        assert_eq!(Parser.parse("fps 24"), Ok(ParserIntent::SetFps { fps: 24 }));
        assert_eq!(Parser.parse("set fps to 120"), Ok(ParserIntent::SetFps { fps: 120 }));
        assert_eq!(Parser.parse("hold 6"), Ok(ParserIntent::SetHold { hold: 6 }));
    }

    #[test]
    fn rejects_zero_positive_values() {
        assert_eq!(Parser.parse("frame 0"), Err(ParserError::ZeroNotAllowed { field: "frame" }));
        assert_eq!(Parser.parse("fps 0"), Err(ParserError::ZeroNotAllowed { field: "fps" }));
        assert_eq!(Parser.parse("hold 0"), Err(ParserError::ZeroNotAllowed { field: "hold" }));
    }

    #[test]
    fn passes_open_ended_work_up_the_stack() {
        assert_eq!(Parser.parse("have GR run from left to right and kick the can"), Ok(ParserIntent::SceneRequest { text: "have GR run from left to right and kick the can".into() }));
    }

    #[test]
    fn does_not_match_inside_another_word() {
        assert_eq!(Parser.parse("fpsboost 12"), Ok(ParserIntent::SceneRequest { text: "fpsboost 12".into() }));
    }
}
