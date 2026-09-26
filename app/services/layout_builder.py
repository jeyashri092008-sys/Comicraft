def build_comic_layout(image_paths: list, full_story: str, outline: list) -> list:
    raw_segments = full_story.split("**Panel")
    story_panels = [f"**Panel {seg}" for seg in raw_segments if seg.strip()]

    while len(story_panels) < len(outline):
        story_panels.append(f"**Panel {len(story_panels)+1}**\n{outline[len(story_panels)].get('scene_description', '')}")

    layout = []
    for idx, (img_path, raw_text, panel_info) in enumerate(zip(image_paths, story_panels, outline), start=1):
        lines = raw_text.strip().splitlines()
        cleaned_text = "\n".join(lines[1:]).strip() if len(lines) > 1 else raw_text.strip()
        layout.append({
            "panel": idx,
            "title": panel_info.get("title", f"Panel {idx}"),
            "image_path": img_path,
            "text": cleaned_text,
            "scene_description": panel_info.get("scene_description", ""),
            "image_prompt": panel_info.get("image_prompt", "")
        })
    return layout
