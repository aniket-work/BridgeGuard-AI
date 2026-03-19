import os
import sys
import time
import random
from PIL import Image, ImageDraw, ImageFont

# Simple Terminal Simulation with PIL
WIDTH, HEIGHT = 1200, 800
BG_COLOR = (24, 24, 24)
TEXT_COLOR = (0, 255, 0)
HEADER_COLOR = (200, 200, 200)

def create_terminal_frame(lines, typing_line="", show_cursor=True):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Draw Window Controls (Mac style)
    draw.ellipse([20, 20, 40, 40], fill=(255, 95, 87))
    draw.ellipse([50, 20, 70, 40], fill=(255, 189, 46))
    draw.ellipse([80, 20, 100, 40], fill=(40, 201, 64))
    
    # Title Bar
    try:
        font = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", 24)
    except:
        font = ImageFont.load_default()
        
    draw.text((120, 20), "BridgeGuard-AI-Terminal — bash", fill=HEADER_COLOR, font=font)
    
    y_offset = 80
    for line in lines:
        draw.text((30, y_offset), line, fill=TEXT_COLOR, font=font)
        y_offset += 35
        
    if typing_line:
        cursor = "_" if show_cursor else ""
        draw.text((30, y_offset), f"$ {typing_line}{cursor}", fill=TEXT_COLOR, font=font)
        
    return img

def create_ui_frame(step_info):
    img = Image.new("RGB", (WIDTH, HEIGHT), (30, 30, 35))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        
    draw.text((WIDTH//2 - 200, 50), "Swarm Orchestrator Dashboard", fill=(255, 255, 255), font=title_font)
    
    # Draw simple graph representation
    nodes = [(300, 300), (500, 300), (700, 300), (400, 500), (600, 500)]
    for i, (x, y) in enumerate(nodes):
        color = (100, 255, 100) if i in step_info['inspected'] else (255, 100, 100)
        draw.ellipse([x-20, y-20, x+20, y+20], fill=color, outline=(255,255,255))
        draw.text((x-5, y-10), str(i), fill=(0,0,0), font=font)
        
    # Draw drones
    for drone in step_info['drones']:
        dx, dy = nodes[drone['pos'] % len(nodes)]
        draw.rectangle([dx-10, dy-40, dx+10, dy-20], fill=(255, 255, 0))
        draw.text((dx-10, dy-70), f"D{drone['id']}", fill=(255, 255, 0), font=font)
        
    # Stats Card
    draw.rectangle([800, 150, 1150, 650], fill=(50, 50, 60))
    draw.text((820, 170), "Swarm Telemetry", fill=(200, 200, 200), font=font)
    draw.text((820, 230), f"Step: {step_info['step']}", fill=(255, 255, 255), font=font)
    draw.text((820, 280), f"Coverage: {len(step_info['inspected'])}/30", fill=(255, 255, 255), font=font)
    
    return img

def generate_gif():
    frames = []
    
    # 1. Terminal Typing
    command = "python simulation.py"
    lines = ["Last login: Wed Mar 18 21:23:09 on ttys001", "dev@macbook medium-publishing % "]
    for i in range(len(command) + 1):
        frames.append(create_terminal_frame(lines, typing_line=command[:i], show_cursor=True))
        
    # 2. Running Simulation Logs
    lines.append(f"dev@macbook medium-publishing % {command}")
    lines.append("--- BridgeGuard-AI: Resilient Infrastructure Swarm Simulation ---")
    lines.append("Total Inspection Points: 30")
    lines.append("Active Drones: 4")
    lines.append("-" * 50)
    
    for i in range(5):
        lines.append(f"Step {i}: Drone {random.randint(1,4)} bidding for Node {random.randint(1,29)}")
        frames.append(create_terminal_frame(lines))
        
    # ASCII Table Summary
    lines.append("-" * 50)
    lines.append("| Drone ID | Status    | Battery | Inspections |")
    lines.append("|----------|-----------|---------|-------------|")
    lines.append("| 1        | IDLE      | 82.5%   | 8           |")
    lines.append("| 2        | MOVING    | 74.0%   | 5           |")
    lines.append("| 3        | IDLE      | 91.0%   | 11          |")
    lines.append("| 4        | ARRIVED   | 68.0%   | 6           |")
    lines.append("-" * 50)
    for _ in range(10): frames.append(create_terminal_frame(lines)) # Hold
    
    # 3. Transition to UI
    # (Just a few blank or fading frames could work, but we'll go direct)
    
    # 4. UI Visualization
    for s in range(10):
        info = {
            "step": s,
            "inspected": random.sample(range(30), s * 2),
            "drones": [{"id": 1, "pos": s % 5}, {"id": 2, "pos": (s+2)%5}]
        }
        frames.append(create_ui_frame(info))
        
    # Save GIF with Global Palette Strategy
    OUTPUT = "images/title-animation.gif"
    os.makedirs("images", exist_ok=True)
    
    # Generate global palette from sample frames
    sample = Image.new("RGB", (WIDTH, HEIGHT * 3))
    sample.paste(frames[0], (0,0)); sample.paste(frames[len(frames)//2], (0,HEIGHT)); sample.paste(frames[-1], (0,HEIGHT*2))
    palette = sample.quantize(colors=256, method=2)
    
    # Convert all frames to P-mode using global palette (No Dither)
    final_frames = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    final_frames[0].save(OUTPUT, save_all=True, append_images=final_frames[1:], optimize=True, loop=0, duration=150)
    print(f"Successfully generated {OUTPUT}")

if __name__ == "__main__":
    generate_gif()
