use std::{path::Path, time::{Duration, Instant}};

use eframe::egui::{self, ColorImage, Context, Pos2, Rect, TextureHandle, TextureOptions, Vec2};

struct AnimatorApp {
    background_path: String,
    character_path: String,
    background: Option<TextureHandle>,
    character: Option<TextureHandle>,
    playing: bool,
    frame: u32,
    fps: u32,
    last_tick: Instant,
    status: String,
}

impl Default for AnimatorApp {
    fn default() -> Self {
        Self {
            background_path: String::new(),
            character_path: String::new(),
            background: None,
            character: None,
            playing: false,
            frame: 0,
            fps: 12,
            last_tick: Instant::now(),
            status: "Load a background PNG and character PNG, then press Play.".into(),
        }
    }
}

impl AnimatorApp {
    fn load_texture(ctx: &Context, path: &str, name: &str) -> Result<TextureHandle, String> {
        let bytes = std::fs::read(Path::new(path)).map_err(|e| format!("{name}: {e}"))?;
        let image = image::load_from_memory(&bytes).map_err(|e| format!("{name}: {e}"))?.to_rgba8();
        let size = [image.width() as usize, image.height() as usize];
        let pixels = image.into_raw();
        let color = ColorImage::from_rgba_unmultiplied(size, &pixels);
        Ok(ctx.load_texture(name.to_owned(), color, TextureOptions::LINEAR))
    }

    fn reload(&mut self, ctx: &Context) {
        match Self::load_texture(ctx, self.background_path.trim(), "background") {
            Ok(tex) => self.background = Some(tex),
            Err(e) => {
                self.status = e;
                return;
            }
        }
        match Self::load_texture(ctx, self.character_path.trim(), "character") {
            Ok(tex) => self.character = Some(tex),
            Err(e) => {
                self.status = e;
                return;
            }
        }
        self.frame = 0;
        self.status = "Loaded. Press Play.".into();
    }
}

impl eframe::App for AnimatorApp {
    fn update(&mut self, ctx: &Context, _frame: &mut eframe::Frame) {
        if self.playing {
            let frame_time = Duration::from_secs_f32(1.0 / self.fps.max(1) as f32);
            if self.last_tick.elapsed() >= frame_time {
                self.frame = (self.frame + 1) % 120;
                self.last_tick = Instant::now();
            }
            ctx.request_repaint_after(frame_time);
        }

        egui::TopBottomPanel::top("controls").show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.label("Background PNG");
                ui.text_edit_singleline(&mut self.background_path);
            });
            ui.horizontal(|ui| {
                ui.label("Character PNG");
                ui.text_edit_singleline(&mut self.character_path);
            });
            ui.horizontal(|ui| {
                if ui.button("Load").clicked() {
                    self.reload(ctx);
                }
                if ui.button(if self.playing { "Pause" } else { "Play" }).clicked() {
                    self.playing = !self.playing;
                    self.last_tick = Instant::now();
                }
                if ui.button("Stop").clicked() {
                    self.playing = false;
                    self.frame = 0;
                }
                ui.label("FPS");
                ui.add(egui::DragValue::new(&mut self.fps).range(1..=60));
                ui.label(format!("Frame {}", self.frame));
            });
            ui.label(&self.status);
        });

        egui::CentralPanel::default().show(ctx, |ui| {
            let available = ui.available_rect_before_wrap();
            let painter = ui.painter_at(available);

            painter.rect_filled(available, 0.0, egui::Color32::from_gray(24));

            if let Some(bg) = &self.background {
                painter.image(
                    bg.id(),
                    available,
                    Rect::from_min_max(Pos2::new(0.0, 0.0), Pos2::new(1.0, 1.0)),
                    egui::Color32::WHITE,
                );
            }

            if let Some(character) = &self.character {
                let size = character.size_vec2();
                let target_h = (available.height() * 0.38).max(48.0);
                let aspect = if size.y > 0.0 { size.x / size.y } else { 1.0 };
                let target = Vec2::new(target_h * aspect, target_h);
                let travel = (available.width() - target.x).max(0.0);
                let t = self.frame as f32 / 119.0;
                let x = available.left() + travel * t;
                let y = available.bottom() - target.y - available.height() * 0.06;
                let rect = Rect::from_min_size(Pos2::new(x, y), target);
                painter.image(
                    character.id(),
                    rect,
                    Rect::from_min_max(Pos2::new(0.0, 0.0), Pos2::new(1.0, 1.0)),
                    egui::Color32::WHITE,
                );
            }
        });
    }
}

fn main() -> eframe::Result<()> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_title("One-Wave Animator")
            .with_inner_size([1280.0, 720.0]),
        ..Default::default()
    };

    eframe::run_native(
        "One-Wave Animator",
        options,
        Box::new(|_cc| Ok(Box::new(AnimatorApp::default()))),
    )
}
