use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Asset {
    pub id: Uuid,
    pub name: String,
    pub kind: AssetKind,
    pub x: f32,
    pub y: f32,
    pub scale: f32,
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub enum AssetKind { Character, Prop }

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Frame {
    pub hold: u8,
    pub assets: Vec<Asset>,
}

impl Default for Frame {
    fn default() -> Self { Self { hold: 1, assets: vec![] } }
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct MotionSequence {
    pub name: String,
    pub character_tag: String,
    pub frames: Vec<Frame>,
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Project {
    pub fps: u8,
    pub active_frame: usize,
    pub background_path: Option<String>,
    pub frames: Vec<Frame>,
    pub motion_library: Vec<MotionSequence>,
}

impl Default for Project {
    fn default() -> Self {
        Self { fps: 12, active_frame: 0, background_path: None, frames: vec![Frame::default()], motion_library: vec![] }
    }
}
