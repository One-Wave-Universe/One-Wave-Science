use std::{io::Write, path::Path, process::{Command, Stdio}};

use serde::{Deserialize, Serialize};

pub const ASSISTANT_PLUGIN_API_VERSION: &str = "one-wave-assistant-plugin/v1";

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct AssistantRequest {
    pub api_version: String,
    pub kind: String,
    pub message: String,
}

impl AssistantRequest {
    pub fn director(message: impl Into<String>) -> Self {
        Self {
            api_version: ASSISTANT_PLUGIN_API_VERSION.to_string(),
            kind: "director".into(),
            message: message.into(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct AssistantResponse {
    pub api_version: String,
    pub ok: bool,
    pub message: String,
}

pub fn invoke_plugin(executable: &Path, request: &AssistantRequest) -> Result<AssistantResponse, String> {
    let mut child = Command::new(executable)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("plugin launch failed: {e}"))?;

    let payload = serde_json::to_vec(request).map_err(|e| format!("plugin request encode failed: {e}"))?;
    child
        .stdin
        .as_mut()
        .ok_or_else(|| "plugin stdin unavailable".to_string())?
        .write_all(&payload)
        .map_err(|e| format!("plugin stdin failed: {e}"))?;

    let output = child.wait_with_output().map_err(|e| format!("plugin wait failed: {e}"))?;
    if !output.status.success() {
        return Err(format!(
            "plugin exited with {}: {}",
            output.status,
            String::from_utf8_lossy(&output.stderr).trim()
        ));
    }

    serde_json::from_slice::<AssistantResponse>(&output.stdout)
        .map_err(|e| format!("plugin response decode failed: {e}"))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn request_contract_is_provider_neutral_and_versioned() {
        let request = AssistantRequest::director("move GR right");
        assert_eq!(request.api_version, ASSISTANT_PLUGIN_API_VERSION);
        assert_eq!(request.kind, "director");
        assert_eq!(request.message, "move GR right");
    }

    #[test]
    fn response_round_trips_as_json() {
        let response = AssistantResponse {
            api_version: ASSISTANT_PLUGIN_API_VERSION.into(),
            ok: true,
            message: "accepted".into(),
        };
        let encoded = serde_json::to_vec(&response).unwrap();
        let decoded: AssistantResponse = serde_json::from_slice(&encoded).unwrap();
        assert_eq!(decoded, response);
    }
}
