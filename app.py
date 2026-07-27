import streamlit as st
from crewai import Agent, Task, Crew, LLM
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import time

# ================== 🔑 OPENROUTER API KEY ==================
OPENROUTER_API_KEY = ""
# ===========================================================

st.set_page_config(
    page_title="NeuralBlog AI — Snehal Jadhav",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── GLOBAL ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { scroll-behavior: smooth; overflow-x: hidden; }

.stApp {
    background: #010208 !important;
    color: #ffffff !important;
    font-family: 'Rajdhani', sans-serif !important;
    overflow-x: hidden;
}

/* Remove all default streamlit top padding */
.main .block-container {
    position: relative; z-index: 1;
    max-width: 1200px !important;
    padding: 0 2rem 3rem !important;
    margin-top: 0 !important;
}
[data-testid="stAppViewContainer"] { padding-top: 0 !important; }
[data-testid="stHeader"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ══════════════════════════════════════════════
   SPLASH SCREEN — exact replica of the hero
══════════════════════════════════════════════ */
#splash {
    position: fixed;
    inset: 0;
    z-index: 999999;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    /* fade out after 4s */
    animation: splashExit 0.9s cubic-bezier(0.7,0,1,1) 4.2s forwards;
}

@keyframes splashExit {
    0%   { opacity: 1;  transform: scale(1);    pointer-events: all; }
    100% { opacity: 0;  transform: scale(1.06); pointer-events: none; visibility: hidden; }
}

/* Splash — same deep-blue bg as main app */
.splash-bg {
    position: absolute; inset: 0;
    background: #010208;
}
.splash-bg::before {
    content: '';
    position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 100% 70% at -5% -5%,  rgba(0,70,220,0.55) 0%, transparent 55%),
        radial-gradient(ellipse 80%  60% at 105% 105%, rgba(0,50,180,0.5)  0%, transparent 55%),
        radial-gradient(ellipse 60%  50% at 50% 0%,    rgba(0,110,255,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 50%  40% at 80% 30%,   rgba(0,140,255,0.1) 0%, transparent 50%);
    animation: splashBgPulse 3s ease-in-out infinite alternate;
}
@keyframes splashBgPulse {
    from { opacity:0.85; } to { opacity:1; }
}

/* Grid overlay identical to main */
.splash-bg::after {
    content: '';
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(0,100,255,0.055) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,100,255,0.055) 1px, transparent 1px),
        linear-gradient(rgba(0,90,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,90,255,0.025) 1px, transparent 1px);
    background-size: 80px 80px, 80px 80px, 20px 20px, 20px 20px;
    animation: gridDriftSplash 18s linear infinite;
}
@keyframes gridDriftSplash {
    0%   { background-position: 0 0,0 0,0 0,0 0; }
    100% { background-position: 80px 80px,80px 80px,20px 20px,20px 20px; }
}

/* Floating orbs in splash */
.splash-orb {
    position: absolute; border-radius: 50%; filter: blur(70px);
    pointer-events: none;
}
.s-orb-1 {
    width:580px; height:580px; opacity:0.2;
    background: radial-gradient(circle, #0077ff, #0022bb 50%, transparent 70%);
    top:-140px; left:-140px;
    animation: sOrb1 16s ease-in-out infinite;
}
.s-orb-2 {
    width:380px; height:380px; opacity:0.15;
    background: radial-gradient(circle, #00aaff, #0044cc 50%, transparent 70%);
    bottom:-80px; right:-80px;
    animation: sOrb2 12s ease-in-out infinite;
}
@keyframes sOrb1 { 0%,100%{transform:translate(0,0);} 50%{transform:translate(60px,80px);} }
@keyframes sOrb2 { 0%,100%{transform:translate(0,0);} 50%{transform:translate(-60px,-50px);} }

/* Horizontal scan line crossing the splash */
.splash-scanline {
    position: absolute;
    top: 0; left: -100%; width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0,160,255,0.9), rgba(100,220,255,1), rgba(0,160,255,0.9), transparent);
    animation: splashScan 2.5s ease-in-out 0.5s infinite;
    z-index: 2;
}
@keyframes splashScan {
    0%   { left:-100%; opacity:0; }
    5%   { opacity:1; }
    95%  { opacity:1; }
    100% { left:100%; opacity:0; }
}

/* Expanding rings behind the text */
.splash-rings {
    position: absolute; inset: 0;
    display: flex; align-items: center; justify-content: center;
    pointer-events: none; z-index: 1;
}
.sring {
    position: absolute; border-radius: 50%;
    border: 1px solid rgba(0,130,255,0.18);
    animation: sRingPulse 3s ease-out infinite;
}
.sring:nth-child(1){width:320px;  height:160px; animation-delay:0s;}
.sring:nth-child(2){width:600px;  height:260px; animation-delay:0.7s;}
.sring:nth-child(3){width:920px;  height:360px; animation-delay:1.4s;}
.sring:nth-child(4){width:1300px; height:480px; animation-delay:2.1s;}
@keyframes sRingPulse {
    0%   { transform:scale(0.6); opacity:0.7; }
    100% { transform:scale(1.1); opacity:0; }
}

/* ── SPLASH CONTENT ── */
.splash-content {
    position: relative; z-index: 10;
    display: flex; flex-direction: column;
    align-items: center; text-align: center;
    padding: 0 2rem;
    width: 100%;
}

/* Badge — same as main eyebrow */
.splash-badge {
    display: inline-flex; align-items: center; gap: 0.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; letter-spacing: 0.3em; text-transform: uppercase;
    color: #55ccff;
    border: 1px solid rgba(0,160,255,0.5);
    padding: 0.35rem 1.2rem; border-radius: 2px;
    background: rgba(0,70,200,0.15);
    box-shadow: 0 0 16px rgba(0,120,255,0.25), inset 0 0 10px rgba(0,100,255,0.08);
    margin-bottom: 1.6rem;
    /* staggered reveal */
    opacity: 0;
    animation: splashItemIn 0.7s cubic-bezier(0.16,1,0.3,1) 0.3s forwards;
}
.sblink {
    width:6px; height:6px; border-radius:50%;
    background:#00ccff; box-shadow:0 0 8px #00ccff, 0 0 16px rgba(0,200,255,0.5);
    animation: blinkF 0.9s ease-in-out infinite;
}
@keyframes blinkF { 0%,100%{opacity:1;} 50%{opacity:0.1;} }

/* "POWERED BY CREWAI" label */
.splash-powered {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(0.75rem,1.8vw,1.1rem); font-weight: 400;
    letter-spacing: 0.55em; text-transform: uppercase;
    color: rgba(0,180,255,0.65);
    margin-bottom: 0.2rem;
    opacity: 0;
    animation: splashItemIn 0.7s cubic-bezier(0.16,1,0.3,1) 0.55s forwards;
}

/* NEURALBLOG AI — giant title */
.splash-title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(4rem, 11vw, 9.5rem);
    font-weight: 900;
    line-height: 0.88;
    letter-spacing: -0.02em;
    text-transform: uppercase;
    display: flex; align-items: flex-start; gap: 0;
    opacity: 0;
    animation: splashTitleReveal 1s cubic-bezier(0.16,1,0.3,1) 0.75s forwards;
    margin-bottom: 0;
}

@keyframes splashTitleReveal {
    from { opacity:0; transform:translateY(40px) scale(0.94); filter:blur(12px); }
    to   { opacity:1; transform:translateY(0) scale(1);        filter:blur(0); }
}

.sn-neural {
    color: #ffffff;
    text-shadow:
        0 0 25px rgba(0,160,255,1),
        0 0 50px rgba(0,120,255,0.7),
        0 0 90px rgba(0,90,255,0.35),
        0 0 140px rgba(0,70,255,0.15);
}

.sn-blog {
    background: linear-gradient(160deg, #55ccff 0%, #aaeeff 25%, #ffffff 48%, #88ddff 68%, #0099ff 88%);
    background-size: 250% 100%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    filter: drop-shadow(0 0 18px rgba(0,160,255,0.85));
    animation: splashBlogShimmer 1.8s ease-in-out 1.8s infinite;
}
@keyframes splashBlogShimmer {
    0%,100% { background-position:250% center; }
    50%      { background-position:0% center; }
}

.sn-ai {
    font-size: 0.42em;
    vertical-align: super;
    margin-top: 0.4em;
    color: #00ccff;
    font-weight: 700; letter-spacing: 0.1em;
    text-shadow: 0 0 15px rgba(0,200,255,1), 0 0 35px rgba(0,160,255,0.6);
    -webkit-text-fill-color: #00ccff;
}

/* Subtitle line */
.splash-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(0.75rem, 1.8vw, 1rem);
    font-weight: 300; letter-spacing: 0.38em; text-transform: uppercase;
    color: rgba(100,200,255,0.55);
    margin-top: 1.1rem;
    opacity: 0;
    animation: splashItemIn 0.7s cubic-bezier(0.16,1,0.3,1) 1.4s forwards;
}

/* Thin glowing divider */
.splash-line {
    width: 0; height: 1px; margin: 1.6rem 0 2rem;
    background: linear-gradient(90deg, transparent, rgba(0,140,255,0.8), rgba(0,220,255,1), rgba(0,140,255,0.8), transparent);
    box-shadow: 0 0 12px rgba(0,160,255,0.5);
    animation: splashLineGrow 0.8s ease-out 1.7s forwards;
}
@keyframes splashLineGrow { to { width: min(600px, 80vw); } }

/* Loading bar */
.splash-loader-wrap {
    width: min(320px, 70vw); height: 2px;
    background: rgba(0,80,200,0.18);
    border-radius: 2px; overflow: hidden;
    opacity: 0;
    animation: splashItemIn 0.5s ease 2s forwards;
}
.splash-loader-fill {
    height: 100%; width: 0;
    background: linear-gradient(90deg, #0055ff, #00aaff, #55eeff, #00aaff, #0055ff);
    background-size: 300% 100%;
    border-radius: 2px;
    animation: loaderGrow 2s ease 2.1s forwards, loaderShimmer 0.6s linear 2.1s infinite;
    box-shadow: 0 0 8px rgba(0,160,255,0.7);
}
@keyframes loaderGrow    { to { width:100%; } }
@keyframes loaderShimmer { 0%{background-position:300% center;} 100%{background-position:0% center;} }

.splash-loading-txt {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem; letter-spacing: 0.3em; text-transform: uppercase;
    color: rgba(0,160,255,0.55);
    margin-top: 0.7rem;
    opacity: 0;
    animation: splashItemIn 0.5s ease 2.2s forwards;
}

@keyframes splashItemIn {
    from { opacity:0; transform:translateY(10px); }
    to   { opacity:1; transform:translateY(0); }
}

/* ══════════════════════════════════════════════
   MAIN APP — appears after splash exits
══════════════════════════════════════════════ */
.stApp-inner {
    opacity: 0;
    animation: appReveal 0.9s ease 5s forwards;
}
@keyframes appReveal {
    from { opacity:0; transform:translateY(8px); }
    to   { opacity:1; transform:translateY(0); }
}

/* ══════════════════════════════════════════════
   BACKGROUND (main app)
══════════════════════════════════════════════ */
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 100% 70% at -5% -5%,  rgba(0,80,255,0.35) 0%, transparent 55%),
        radial-gradient(ellipse 80%  60% at 105% 105%, rgba(0,60,200,0.4)  0%, transparent 55%),
        radial-gradient(ellipse 60%  50% at 50% 0%,    rgba(0,120,255,0.15) 0%, transparent 60%),
        radial-gradient(ellipse 50%  40% at 80% 30%,   rgba(0,160,255,0.08) 0%, transparent 50%),
        radial-gradient(ellipse 30%  30% at 20% 80%,   rgba(0,100,255,0.1)  0%, transparent 50%);
    animation: nebulaShift 10s ease-in-out infinite alternate;
    pointer-events: none; z-index: 0;
}
@keyframes nebulaShift {
    0%   { opacity:0.8;  filter:hue-rotate(0deg) brightness(1); }
    50%  { opacity:1;    filter:hue-rotate(12deg) brightness(1.1); }
    100% { opacity:0.85; filter:hue-rotate(-8deg) brightness(0.95); }
}
.stApp::after {
    content: '';
    position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(0,120,255,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,120,255,0.06) 1px, transparent 1px),
        linear-gradient(rgba(0,100,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,100,255,0.03) 1px, transparent 1px);
    background-size: 80px 80px, 80px 80px, 20px 20px, 20px 20px;
    animation: gridDrift 18s linear infinite;
    pointer-events: none; z-index: 0;
}
@keyframes gridDrift {
    0%   { background-position:0 0,0 0,0 0,0 0; }
    100% { background-position:80px 80px,80px 80px,20px 20px,20px 20px; }
}

/* Orbs */
.orb-container { position:fixed; inset:0; pointer-events:none; z-index:0; overflow:hidden; }
.orb { position:absolute; border-radius:50%; filter:blur(70px); }
.orb-1{width:600px;height:600px;opacity:.18;background:radial-gradient(circle,#0088ff,#0033cc 50%,transparent 70%);top:-150px;left:-150px;animation:oF1 16s ease-in-out infinite;}
.orb-2{width:400px;height:400px;opacity:.15;background:radial-gradient(circle,#00bbff,#0055dd 50%,transparent 70%);top:35%;right:-100px;animation:oF2 12s ease-in-out infinite;}
.orb-3{width:300px;height:300px;opacity:.12;background:radial-gradient(circle,#55aaff,#0044bb 50%,transparent 70%);bottom:5%;left:25%;animation:oF3 19s ease-in-out infinite;}
.orb-4{width:200px;height:200px;opacity:.1;background:radial-gradient(circle,#00ddff,#0066cc 50%,transparent 70%);top:60%;left:55%;animation:oF1 22s ease-in-out infinite reverse;}
@keyframes oF1{0%,100%{transform:translate(0,0) scale(1);}33%{transform:translate(70px,90px) scale(1.1);}66%{transform:translate(-50px,130px) scale(.92);}}
@keyframes oF2{0%,100%{transform:translate(0,0);}50%{transform:translate(-90px,-70px) scale(1.15);}}
@keyframes oF3{0%,100%{transform:translate(0,0);}40%{transform:translate(60px,-50px);}80%{transform:translate(-35px,35px);}}

/* ══════════════════════════════════════════════
   HERO (main, same look as splash)
══════════════════════════════════════════════ */
.hero-section {
    position: relative; text-align: center;
    /* tight padding so hero is fully visible on load */
    padding: 2.8rem 1rem 2.2rem;
    overflow: hidden;
    min-height: auto;
}
.hero-section::before {
    content:'';
    position:absolute; top:0; left:-100%; width:100%; height:2px;
    background:linear-gradient(90deg,transparent,rgba(0,160,255,.9),rgba(100,220,255,1),rgba(0,160,255,.9),transparent);
    animation:scanLine 3.5s ease-in-out infinite;
}
@keyframes scanLine{0%{left:-100%;opacity:0;}10%{opacity:1;}90%{opacity:1;}100%{left:100%;opacity:0;}}

.hero-eyebrow {
    display:inline-flex; align-items:center; gap:.5rem;
    font-family:'JetBrains Mono',monospace; font-size:.63rem;
    letter-spacing:.3em; text-transform:uppercase; color:#55ccff;
    border:1px solid rgba(0,160,255,.5); padding:.35rem 1.2rem;
    border-radius:2px; margin-bottom:1.5rem;
    background:rgba(0,80,255,.12);
    box-shadow:0 0 15px rgba(0,120,255,.2),inset 0 0 10px rgba(0,100,255,.08);
    animation:heroIn .8s cubic-bezier(.16,1,.3,1) 5.2s both;
}
@keyframes heroIn{from{opacity:0;transform:translateY(-14px);}to{opacity:1;transform:translateY(0);}}
.dot-blink{width:6px;height:6px;border-radius:50%;background:#00ccff;box-shadow:0 0 8px #00ccff,0 0 16px rgba(0,200,255,.5);animation:blinkF 0.9s ease-in-out infinite;}

.hero-title-top {
    font-family:'Orbitron',sans-serif;
    font-size:clamp(.85rem,2vw,1.15rem); font-weight:400;
    letter-spacing:.55em; text-transform:uppercase;
    color:rgba(0,180,255,.65); margin-bottom:.2rem;
    animation:heroIn .8s cubic-bezier(.16,1,.3,1) 5.35s both;
}

.hero-title-main {
    font-family:'Orbitron',sans-serif;
    font-size:clamp(3.2rem,9vw,8.5rem); font-weight:900;
    line-height:.88; letter-spacing:-.02em; text-transform:uppercase;
    display:inline-flex; align-items:flex-start;
    animation:heroTitleIn 1s cubic-bezier(.16,1,.3,1) 5.5s both;
}
@keyframes heroTitleIn{from{opacity:0;transform:translateY(28px);filter:blur(8px);}to{opacity:1;transform:translateY(0);filter:blur(0);}}

.word-neural{
    color:#ffffff;
    text-shadow:0 0 22px rgba(0,160,255,1),0 0 45px rgba(0,120,255,.7),0 0 85px rgba(0,90,255,.3);
}
.word-blog{
    background:linear-gradient(160deg,#55ccff 0%,#aaeeff 25%,#ffffff 48%,#88ddff 68%,#0099ff 88%);
    background-size:200% 100%;
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
    filter:drop-shadow(0 0 16px rgba(0,160,255,.8));
    animation:shimmer 2.5s ease-in-out 6s infinite;
}
@keyframes shimmer{0%,100%{background-position:200% center;}50%{background-position:0% center;}}
.word-ai{
    font-size:.45em;vertical-align:super;margin-top:.3em;
    color:#00ccff;font-weight:700;letter-spacing:.12em;
    text-shadow:0 0 15px rgba(0,200,255,1),0 0 30px rgba(0,160,255,.5);
    -webkit-text-fill-color:#00ccff;
}
.hero-title-main:hover .word-neural{animation:glitch .35s steps(2) infinite;}
@keyframes glitch{
    0%{text-shadow:3px 0 #0088ff,-3px 0 #55ddff,0 0 20px rgba(0,160,255,.9);}
    25%{text-shadow:-3px 0 #0088ff,3px 0 #55ddff,0 0 20px rgba(0,160,255,.9);}
    50%{text-shadow:3px 2px #0088ff,-3px -2px #55ddff,0 0 20px rgba(0,160,255,.9);}
    75%{text-shadow:-3px 2px #0055ff,3px -2px #55ddff,0 0 20px rgba(0,160,255,.9);}
    100%{text-shadow:3px 0 #0088ff,-3px 0 #55ddff,0 0 20px rgba(0,160,255,.9);}
}

.hero-subtitle{
    font-family:'Rajdhani',sans-serif; font-size:1rem; font-weight:300;
    letter-spacing:.38em; color:rgba(100,200,255,.5); text-transform:uppercase;
    margin-top:1rem;
    animation:heroIn .8s cubic-bezier(.16,1,.3,1) 5.8s both;
}

.divider-line{
    height:1px;
    background:linear-gradient(90deg,transparent,rgba(0,120,255,.7),rgba(0,200,255,1),rgba(0,120,255,.7),transparent);
    margin:.5rem auto 2rem; max-width:580px;
    box-shadow:0 0 10px rgba(0,160,255,.4);
    animation:lineGrow 1s ease 6s both;
}
@keyframes lineGrow{from{transform:scaleX(0);opacity:0;}to{transform:scaleX(1);opacity:1;}}

/* ── STATS RIBBON ── */
.stats-ribbon{
    display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
    background:rgba(0,100,255,.18);border:1px solid rgba(0,140,255,.3);
    border-radius:6px;overflow:hidden;margin-bottom:2rem;
    box-shadow:0 0 20px rgba(0,80,255,.15);
    animation:heroIn .8s ease 6.2s both;
}
.stat-cell{
    background:rgba(0,10,40,.7);padding:1.1rem 1rem;text-align:center;
    position:relative;overflow:hidden;transition:background .3s;
}
.stat-cell:hover{background:rgba(0,30,90,.8);}
.stat-cell::after{
    content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,rgba(0,160,255,.9),rgba(0,220,255,1),transparent);
    transform:scaleX(0);transition:transform .4s;box-shadow:0 0 8px rgba(0,160,255,.6);
}
.stat-cell:hover::after{transform:scaleX(1);}
.stat-number{font-family:'Orbitron',sans-serif;font-size:1.5rem;font-weight:700;color:#fff;line-height:1;letter-spacing:.05em;text-shadow:0 0 12px rgba(0,160,255,.6);}
.stat-label{font-family:'JetBrains Mono',monospace;font-size:.58rem;color:rgba(0,180,255,.6);letter-spacing:.2em;text-transform:uppercase;margin-top:.35rem;}

/* ── SECTION HEADER ── */
.sec-header{display:flex;align-items:center;gap:1rem;margin-bottom:1rem;}
.sec-header-line{flex:1;height:1px;background:linear-gradient(90deg,rgba(0,100,255,.4),transparent);}
.sec-header-text{font-family:'JetBrains Mono',monospace;font-size:.58rem;letter-spacing:.3em;text-transform:uppercase;color:rgba(0,180,255,.7);white-space:nowrap;}
.sec-header-num{font-family:'Orbitron',sans-serif;font-size:.6rem;color:rgba(0,140,255,.6);}

/* ── AGENT NODES ── */
.agents-panel{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:2rem;}
.agent-node{
    position:relative;
    background:linear-gradient(135deg,rgba(0,15,60,.85) 0%,rgba(0,25,80,.7) 100%);
    border:1px solid rgba(0,80,200,.3);border-radius:10px;
    padding:1.4rem 1.2rem 1.2rem;overflow:hidden;
    transition:transform .35s,border-color .35s,box-shadow .35s;
}
.agent-node::before{content:'';position:absolute;top:0;left:0;width:22px;height:22px;border-top:2px solid rgba(0,160,255,.6);border-left:2px solid rgba(0,160,255,.6);border-radius:10px 0 0 0;transition:width .4s,height .4s,border-color .3s;}
.agent-node::after{content:'';position:absolute;bottom:0;right:0;width:22px;height:22px;border-bottom:2px solid rgba(0,160,255,.6);border-right:2px solid rgba(0,160,255,.6);border-radius:0 0 10px 0;transition:width .4s,height .4s,border-color .3s;}
.agent-node:hover{transform:translateY(-6px);border-color:rgba(0,180,255,.7);box-shadow:0 14px 50px rgba(0,80,220,.35),0 0 30px rgba(0,120,255,.1);}
.agent-node:hover::before,.agent-node:hover::after{width:38px;height:38px;border-color:rgba(0,220,255,.9);}
.scan-bar{position:absolute;top:0;left:0;right:0;height:100%;background:linear-gradient(180deg,transparent 0%,rgba(0,120,255,.06) 50%,transparent 100%);transform:translateY(-100%);animation:scanV 3.5s ease-in-out infinite;}
.agent-node:nth-child(2) .scan-bar{animation-delay:1.2s;}
.agent-node:nth-child(3) .scan-bar{animation-delay:2.4s;}
@keyframes scanV{0%{transform:translateY(-100%);}50%{transform:translateY(100%);}100%{transform:translateY(100%);}}
.agent-number{font-family:'JetBrains Mono',monospace;font-size:.5rem;letter-spacing:.3em;color:rgba(0,160,255,.5);margin-bottom:.8rem;}
.agent-icon-wrap{width:48px;height:48px;background:rgba(0,40,160,.4);border:1px solid rgba(0,140,255,.4);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin-bottom:.9rem;box-shadow:0 0 12px rgba(0,100,255,.2);transition:background .3s,border-color .3s,box-shadow .3s;}
.agent-node:hover .agent-icon-wrap{background:rgba(0,60,200,.5);border-color:rgba(0,200,255,.6);box-shadow:0 0 25px rgba(0,160,255,.35);}
.agent-title{font-family:'Orbitron',sans-serif;font-size:.75rem;font-weight:700;color:#fff;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.25rem;text-shadow:0 0 10px rgba(0,140,255,.4);}
.agent-desc{font-family:'Rajdhani',sans-serif;font-size:.75rem;color:rgba(100,180,255,.55);line-height:1.4;}
.agent-status-row{display:flex;align-items:center;gap:.4rem;margin-top:.9rem;}
.status-pip{width:7px;height:7px;border-radius:50%;background:#00aaff;box-shadow:0 0 8px #00aaff,0 0 16px rgba(0,180,255,.4);animation:pipPulse 1.8s ease-in-out infinite;}
@keyframes pipPulse{0%,100%{box-shadow:0 0 5px #00aaff,0 0 10px rgba(0,160,255,.3);opacity:1;}50%{box-shadow:0 0 15px #00ddff,0 0 30px rgba(0,200,255,.5);opacity:.7;}}
.agent-node:nth-child(2) .status-pip{animation-delay:.6s;}
.agent-node:nth-child(3) .status-pip{animation-delay:1.2s;}
.status-label{font-family:'JetBrains Mono',monospace;font-size:.55rem;letter-spacing:.2em;color:rgba(0,180,255,.7);text-transform:uppercase;}
.pipeline-flow{display:flex;align-items:center;justify-content:center;margin:-1.2rem 0 1.8rem;opacity:.5;font-family:'JetBrains Mono',monospace;font-size:.65rem;letter-spacing:.2em;color:rgba(0,160,255,.9);}
.pipeline-flow .arrow{margin:0 .8rem;animation:arrowPulse 1.5s ease-in-out infinite;}
.pipeline-flow .arrow:nth-child(2){animation-delay:.5s;}
.pipeline-flow .arrow:nth-child(4){animation-delay:1s;}
@keyframes arrowPulse{0%,100%{opacity:.3;transform:translateX(0);}50%{opacity:1;transform:translateX(4px);}}

/* ── CHAT INPUT ── */
.stChatInput>div{background:rgba(0,10,50,.75) !important;border:1px solid rgba(0,100,255,.4) !important;border-radius:8px !important;transition:border-color .3s,box-shadow .3s !important;backdrop-filter:blur(12px);}
.stChatInput>div:focus-within{border-color:rgba(0,180,255,.8) !important;box-shadow:0 0 0 3px rgba(0,100,255,.12),0 0 30px rgba(0,120,255,.12) !important;}
.stChatInput textarea{font-family:'Rajdhani',sans-serif !important;font-size:1rem !important;font-weight:500 !important;color:#fff !important;background:transparent !important;letter-spacing:.05em !important;}
.stChatInput textarea::placeholder{color:rgba(0,160,255,.4) !important;}

/* ── TERMINAL ── */
.activity-terminal{background:rgba(0,5,25,.92);border:1px solid rgba(0,100,255,.35);border-radius:8px;padding:1rem 1.4rem;margin:1rem 0;font-family:'JetBrains Mono',monospace;position:relative;overflow:hidden;box-shadow:0 0 20px rgba(0,80,255,.1);animation:termIn .4s ease both;}
@keyframes termIn{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:translateY(0);}}
.activity-terminal::before{content:'';position:absolute;top:0;left:-100%;width:60%;height:1px;background:linear-gradient(90deg,transparent,rgba(0,180,255,.9),rgba(100,220,255,1),transparent);animation:termScan 2s ease-in-out infinite;}
@keyframes termScan{0%{left:-60%;}100%{left:160%;}}
.terminal-header{display:flex;align-items:center;gap:.5rem;margin-bottom:.6rem;padding-bottom:.5rem;border-bottom:1px solid rgba(0,80,255,.2);}
.t-dot{width:8px;height:8px;border-radius:50%;}
.t-dot-1{background:rgba(255,80,80,.7);}.t-dot-2{background:rgba(255,200,60,.7);}.t-dot-3{background:rgba(0,220,100,.7);}
.t-title{font-size:.6rem;letter-spacing:.2em;color:rgba(0,180,255,.6);margin-left:.3rem;text-transform:uppercase;}
.terminal-body{display:flex;align-items:center;gap:.8rem;}
.t-prompt{color:rgba(0,160,255,.8);font-size:.72rem;}.t-text{color:rgba(180,225,255,.9);font-size:.72rem;letter-spacing:.05em;}
.t-cursor{display:inline-block;width:7px;height:13px;background:rgba(0,180,255,.9);box-shadow:0 0 8px rgba(0,160,255,.7);animation:cursorB .7s step-end infinite;margin-left:2px;vertical-align:middle;}
@keyframes cursorB{0%,100%{opacity:1;}50%{opacity:0;}}
.progress-track{margin-top:.8rem;display:grid;grid-template-columns:repeat(3,1fr);gap:6px;}
.progress-step{height:3px;border-radius:2px;background:rgba(0,80,200,.25);position:relative;overflow:hidden;}
.progress-step.active::after{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:linear-gradient(90deg,transparent,#0088ff,#00ddff);animation:fillP .8s ease forwards;box-shadow:0 0 6px rgba(0,160,255,.8);}
.progress-step.done{background:rgba(0,120,255,.5);box-shadow:0 0 8px rgba(0,160,255,.5);}
@keyframes fillP{to{left:0;}}

/* ── MESSAGES ── */
.stChatMessage{background:transparent !important;border:none !important;}
[data-testid="stChatMessageContent"]{background:rgba(0,8,40,.65) !important;border:1px solid rgba(0,80,200,.25) !important;border-radius:8px !important;padding:1.3rem 1.6rem !important;font-family:'Rajdhani',sans-serif !important;font-size:.95rem !important;color:rgba(220,240,255,.93) !important;line-height:1.8 !important;animation:msgR .5s cubic-bezier(.16,1,.3,1) both;backdrop-filter:blur(8px);}
[data-testid="stChatMessageContent"] p{font-family:'Rajdhani',sans-serif !important;font-size:.95rem !important;color:rgba(220,240,255,.93) !important;}
@keyframes msgR{from{opacity:0;transform:translateY(12px) scale(.99);}to{opacity:1;transform:translateY(0) scale(1);}}
[data-testid="chat-message-user"] [data-testid="stChatMessageContent"]{border-color:rgba(0,130,255,.4) !important;background:rgba(0,20,80,.55) !important;}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton>button{position:relative;background:transparent !important;color:#fff !important;font-family:'Orbitron',sans-serif !important;font-weight:700 !important;font-size:.72rem !important;letter-spacing:.2em !important;text-transform:uppercase !important;border:1px solid rgba(0,140,255,.6) !important;border-radius:6px !important;padding:.85rem 2.5rem !important;overflow:hidden !important;transition:border-color .3s,box-shadow .3s !important;box-shadow:0 0 15px rgba(0,100,255,.15) !important;}
.stDownloadButton>button:hover{border-color:rgba(0,200,255,.9) !important;box-shadow:0 0 30px rgba(0,140,255,.4),0 0 60px rgba(0,100,255,.2) !important;}

/* ── FOOTER ── */
.app-footer{margin-top:3rem;padding:2rem 0;text-align:center;border-top:1px solid rgba(0,80,200,.2);}
.footer-grid-text{font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:.3em;text-transform:uppercase;color:rgba(0,140,255,.4);line-height:2;}
.footer-copyright{font-family:'Orbitron',sans-serif;font-size:.65rem;font-weight:600;letter-spacing:.25em;color:rgba(0,180,255,.65);margin-top:.3rem;text-transform:uppercase;text-shadow:0 0 12px rgba(0,140,255,.4);}

/* ── MISC ── */
.stSpinner>div{border-top-color:#0099ff !important;}
::-webkit-scrollbar{width:5px;}::-webkit-scrollbar-track{background:rgba(0,5,30,.5);}::-webkit-scrollbar-thumb{background:rgba(0,80,200,.5);border-radius:3px;}::-webkit-scrollbar-thumb:hover{background:rgba(0,140,255,.7);}
#MainMenu,footer,header,.stDeployButton{visibility:hidden !important;display:none !important;}
</style>

<!-- ════════════════════════════
     SPLASH SCREEN
════════════════════════════ -->
<div id="splash">
    <div class="splash-bg"></div>
    <!-- orbs -->
    <div class="splash-orb s-orb-1"></div>
    <div class="splash-orb s-orb-2"></div>
    <!-- rings -->
    <div class="splash-rings">
        <div class="sring"></div>
        <div class="sring"></div>
        <div class="sring"></div>
        <div class="sring"></div>
    </div>
    <!-- scanline -->
    <div class="splash-scanline"></div>
    <!-- content -->
    <div class="splash-content">
        <div class="splash-badge">
            <div class="sblink"></div>
            Multi-Agent Content System &nbsp;·&nbsp; V3.0
        </div>
        <div class="splash-powered">Powered by CrewAI</div>
        <div class="splash-title">
            <span class="sn-neural">NEURAL</span><span class="sn-blog">BLOG</span><sup class="sn-ai">AI</sup>
        </div>
        <div class="splash-sub">Three Agents &nbsp;·&nbsp; One Perfect Article &nbsp;·&nbsp; Zero Effort</div>
        <div class="splash-line"></div>
        <div class="splash-loader-wrap">
            <div class="splash-loader-fill"></div>
        </div>
        <div class="splash-loading-txt">Initializing agent network...</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── ORBS ──
st.markdown("""
<div class="orb-container">
    <div class="orb orb-1"></div><div class="orb orb-2"></div>
    <div class="orb orb-3"></div><div class="orb orb-4"></div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════
# HERO — visible immediately on load (no scroll)
# ════════════════════════════════════════
st.markdown("""
<div class="hero-section">
    <div class="hero-eyebrow">
        <div class="dot-blink"></div>
        Multi-Agent Content System &nbsp;·&nbsp; V3.0
    </div>
    <div class="hero-title-top">Powered by CrewAI</div>
    <div class="hero-title-main">
        <span class="word-neural">NEURAL</span><span class="word-blog">BLOG</span><sup class="word-ai">AI</sup>
    </div>
    <div class="hero-subtitle">Three Agents &nbsp;·&nbsp; One Perfect Article &nbsp;·&nbsp; Zero Effort</div>
</div>
<div class="divider-line"></div>
""", unsafe_allow_html=True)

# ── STATS ──
st.markdown("""
<div class="stats-ribbon">
    <div class="stat-cell"><div class="stat-number">03</div><div class="stat-label">AI Agents</div></div>
    <div class="stat-cell"><div class="stat-number">LLM</div><div class="stat-label">Llama-3 8B</div></div>
    <div class="stat-cell"><div class="stat-number">SEO</div><div class="stat-label">Optimized</div></div>
    <div class="stat-cell"><div class="stat-number">PDF</div><div class="stat-label">Export Ready</div></div>
</div>
""", unsafe_allow_html=True)

# ── AGENTS ──
st.markdown("""
<div class="sec-header">
    <div class="sec-header-num">01</div>
    <div class="sec-header-line"></div>
    <div class="sec-header-text">Autonomous Agent Network</div>
    <div class="sec-header-line"></div>
</div>
<div class="agents-panel">
    <div class="agent-node">
        <div class="scan-bar"></div>
        <div class="agent-number">AGENT // 001</div>
        <div class="agent-icon-wrap">🧭</div>
        <div class="agent-title">Planner</div>
        <div class="agent-desc">SEO strategy, keyword mapping &amp; structural outline architect</div>
        <div class="agent-status-row"><div class="status-pip"></div><div class="status-label">Standby</div></div>
    </div>
    <div class="agent-node">
        <div class="scan-bar"></div>
        <div class="agent-number">AGENT // 002</div>
        <div class="agent-icon-wrap">✍️</div>
        <div class="agent-title">Writer</div>
        <div class="agent-desc">Long-form article generation with narrative depth &amp; engagement</div>
        <div class="agent-status-row"><div class="status-pip"></div><div class="status-label">Standby</div></div>
    </div>
    <div class="agent-node">
        <div class="scan-bar"></div>
        <div class="agent-number">AGENT // 003</div>
        <div class="agent-icon-wrap">🔍</div>
        <div class="agent-title">Editor</div>
        <div class="agent-desc">Grammar, clarity, flow enhancement &amp; publication-grade polish</div>
        <div class="agent-status-row"><div class="status-pip"></div><div class="status-label">Standby</div></div>
    </div>
</div>
<div class="pipeline-flow">
    <span>PLAN</span><span class="arrow">──▶</span>
    <span>WRITE</span><span class="arrow">──▶</span>
    <span>EDIT</span><span class="arrow">──▶</span>
    <span>OUTPUT</span>
</div>
""", unsafe_allow_html=True)

# ── LLM ──
llm = LLM(
    model="openrouter/meta-llama/llama-3-8b-instruct",
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# ── SESSION STATE ──
for key, default in [("chat_history",[]),("final_output",""),("blog_count",0),("total_words",0)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── INPUT ──
st.markdown("""
<div class="sec-header" style="margin-top:.5rem;">
    <div class="sec-header-num">02</div>
    <div class="sec-header-line"></div>
    <div class="sec-header-text">Topic Input Terminal</div>
    <div class="sec-header-line"></div>
</div>
""", unsafe_allow_html=True)

user_input = st.chat_input("Input blog topic → agents activate automatically...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    act_ph  = st.empty()
    prog_ph = st.empty()
    steps_info = [
        ("001 // PLANNER", "Mapping keywords · Building SEO architecture · Structuring outline..."),
        ("002 // WRITER",  "Generating long-form content · Weaving narrative depth · Adding detail..."),
        ("003 // EDITOR",  "Refining grammar · Enhancing flow · Final publication polish..."),
    ]
    act_ph.markdown("""
    <div class="activity-terminal">
        <div class="terminal-header">
            <div class="t-dot t-dot-1"></div><div class="t-dot t-dot-2"></div><div class="t-dot t-dot-3"></div>
            <div class="t-title">neuralblog.ai — pipeline.exe</div>
        </div>
        <div class="terminal-body">
            <div class="t-prompt">▶</div>
            <div class="t-text">INITIALIZING MULTI-AGENT PIPELINE<div class="t-cursor"></div></div>
        </div>
        <div class="progress-track">
            <div class="progress-step"></div><div class="progress-step"></div><div class="progress-step"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner(""):
        for i,(agent_id,action_text) in enumerate(steps_info):
            sh = "".join(f'<div class="progress-step {"done" if j<i else ("active" if j==i else "")}"></div>' for j in range(3))
            prog_ph.markdown(f"""
            <div class="activity-terminal">
                <div class="terminal-header">
                    <div class="t-dot t-dot-1"></div><div class="t-dot t-dot-2"></div><div class="t-dot t-dot-3"></div>
                    <div class="t-title">STEP {i+1} / 3 — AGENT {agent_id}</div>
                </div>
                <div class="terminal-body">
                    <div class="t-prompt">▶</div>
                    <div class="t-text">{action_text}<div class="t-cursor"></div></div>
                </div>
                <div class="progress-track">{sh}</div>
            </div>""", unsafe_allow_html=True)
            time.sleep(0.5)

        planner = Agent(role="Content Planner",goal="Create structured blog outline on {topic}",backstory="Elite SEO strategist with a decade of experience.",llm=llm,verbose=False)
        writer  = Agent(role="Content Writer",goal="Write a detailed, engaging, long-form blog article from the given outline",backstory="Award-winning long-form journalist turned digital content specialist.",llm=llm,verbose=False)
        editor  = Agent(role="Editor",goal="Polish grammar, clarity, tone and overall reader experience",backstory="Former chief editor at major digital publication.",llm=llm,verbose=False)
        task1 = Task(description="Create a comprehensive SEO-optimized blog outline for topic: {topic}. Include H1, H2, H3, key points, meta description and 8–10 target keywords.",expected_output="Detailed structured outline.",agent=planner)
        task2 = Task(description="Write a complete blog article (900–1300 words) with compelling hook, rich body paragraphs and strong CTA conclusion.",expected_output="Complete publish-ready blog article.",agent=writer)
        task3 = Task(description="Edit and polish the full article. Fix grammar, enhance sentence variety, improve transitions. Output only the final article.",expected_output="Final polished article.",agent=editor)
        crew = Crew(agents=[planner,writer,editor],tasks=[task1,task2,task3],verbose=False)
        result = crew.kickoff(inputs={"topic": user_input})
        final_text = str(result)
        wc = len(final_text.split())
        st.session_state.blog_count  += 1
        st.session_state.total_words += wc
        st.session_state.final_output = final_text
        st.session_state.chat_history.append(("assistant", final_text))

    act_ph.markdown(f"""
    <div class="activity-terminal" style="border-color:rgba(0,160,255,.6);box-shadow:0 0 25px rgba(0,120,255,.2);">
        <div class="terminal-header">
            <div class="t-dot t-dot-1"></div><div class="t-dot t-dot-2"></div><div class="t-dot t-dot-3"></div>
            <div class="t-title">PIPELINE COMPLETE</div>
        </div>
        <div class="terminal-body">
            <div class="t-prompt" style="color:#00ddff;">✓</div>
            <div class="t-text" style="color:rgba(150,220,255,.95);">ALL 3 AGENTS COMPLETED &nbsp;·&nbsp; {wc} WORDS GENERATED &nbsp;·&nbsp; ARTICLE READY</div>
        </div>
        <div class="progress-track">
            <div class="progress-step done"></div><div class="progress-step done"></div><div class="progress-step done"></div>
        </div>
    </div>""", unsafe_allow_html=True)
    prog_ph.empty()

# ── OUTPUT ──
if st.session_state.chat_history:
    st.markdown("""
    <div class="sec-header" style="margin-top:2rem;">
        <div class="sec-header-num">03</div>
        <div class="sec-header-line"></div>
        <div class="sec-header-text">Generated Output</div>
        <div class="sec-header-line"></div>
    </div>""", unsafe_allow_html=True)
    for role,message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

# ── PDF ──
def generate_pdf(text):
    path = "/tmp/NeuralBlog_SnehalJadhav.pdf"
    doc = SimpleDocTemplate(path,pagesize=A4,leftMargin=65,rightMargin=65,topMargin=65,bottomMargin=65)
    styles = getSampleStyleSheet()
    ts=styles["Title"];ts.fontName="Helvetica-Bold";ts.fontSize=20;ts.leading=26;ts.spaceAfter=8
    sub=styles["Italic"];sub.fontSize=9;sub.spaceAfter=20
    bs=styles["Normal"];bs.fontName="Helvetica";bs.fontSize=10.5;bs.leading=17;bs.spaceAfter=8
    hs=styles["Heading2"];hs.fontName="Helvetica-Bold";hs.fontSize=13;hs.leading=18;hs.spaceBefore=14;hs.spaceAfter=6
    elems=[Paragraph("NeuralBlog AI — Generated Article",ts),Paragraph("Powered by CrewAI + Llama-3  |  © Snehal Jadhav  |  All Rights Reserved",sub),Spacer(1,10)]
    for line in text.split("\n"):
        s=line.strip()
        if not s: elems.append(Spacer(1,5))
        elif s.startswith("###"): elems.append(Paragraph(s.lstrip("#").strip(),hs))
        elif s.startswith("##"):  elems.append(Paragraph(f"<b>{s.lstrip('#').strip()}</b>",hs))
        elif s.startswith("#"):   elems.append(Paragraph(s.lstrip("#").strip(),ts))
        else:                     elems.append(Paragraph(s,bs))
    doc.build(elems)
    return path

if st.session_state.final_output:
    st.markdown("""
    <div class="sec-header" style="margin-top:2rem;">
        <div class="sec-header-num">04</div>
        <div class="sec-header-line"></div>
        <div class="sec-header-text">Export Article</div>
        <div class="sec-header-line"></div>
    </div>""", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1.8,2,1.8])
    with c2:
        pdf_path = generate_pdf(st.session_state.final_output)
        with open(pdf_path,"rb") as f:
            st.download_button("⬇  EXPORT AS PDF",f,file_name="NeuralBlog_AI_SnehalJadhav.pdf",mime="application/pdf",use_container_width=True)

# ── FOOTER ──
st.markdown("""
<div class="app-footer">
    <div class="footer-grid-text">NeuralBlog AI &nbsp;·&nbsp; Multi-Agent Content Engine &nbsp;·&nbsp; Powered by CrewAI + OpenRouter + Llama-3 8B</div>
    <div class="footer-copyright">© 2025 Snehal Jadhav &nbsp;·&nbsp; All Rights Reserved</div>
</div>
""", unsafe_allow_html=True)
