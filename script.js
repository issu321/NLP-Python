/* ═══════════════════════════════════════════════════════════════
   FAKE NEWS DETECTOR — INTERACTIVE ENGINE
   Author: Ussu | GitHub: https://github.com/issu321
   Repo: https://github.com/issu321/NLP-Python
   ═══════════════════════════════════════════════════════════════ */

(function() {
    'use strict';

    const state = { currentPage: 0, totalPages: 6, isAnimating: false, charts: {} };
    const $ = (sel) => document.querySelector(sel);
    const $$ = (sel) => document.querySelectorAll(sel);

    // ─── CUSTOM CURSOR ───
    function initCursor() {
        if (window.matchMedia('(pointer: coarse)').matches) return;
        const dot = $('.cursor-dot');
        const outline = $('.cursor-outline');
        if (!dot || !outline) return;
        let mouseX = 0, mouseY = 0, outlineX = 0, outlineY = 0;
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX; mouseY = e.clientY;
            dot.style.left = mouseX + 'px';
            dot.style.top = mouseY + 'px';
        });
        function animateOutline() {
            outlineX += (mouseX - outlineX) * 0.15;
            outlineY += (mouseY - outlineY) * 0.15;
            outline.style.left = outlineX + 'px';
            outline.style.top = outlineY + 'px';
            requestAnimationFrame(animateOutline);
        }
        animateOutline();
    }

    // ─── BACKGROUND CANVAS ───
    function initCanvas() {
        const canvas = $('#bgCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let particles = [];
        const PARTICLE_COUNT = window.innerWidth < 768 ? 30 : 60;
        const CONNECTION_DIST = 120;
        const MOUSE_DIST = 150;
        let mouse = { x: null, y: null };
        function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
        resize(); window.addEventListener('resize', resize);

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (Math.random() - 0.5) * 0.5;
                this.vy = (Math.random() - 0.5) * 0.5;
                this.size = Math.random() * 2 + 1;
                this.baseColor = Math.random() > 0.5 ? '6,182,212' : '139,92,246';
            }
            update() {
                this.x += this.vx; this.y += this.vy;
                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
                if (mouse.x !== null) {
                    const dx = mouse.x - this.x, dy = mouse.y - this.y;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    if (dist < MOUSE_DIST) {
                        const force = (MOUSE_DIST - dist) / MOUSE_DIST;
                        this.vx -= (dx / dist) * force * 0.02;
                        this.vy -= (dy / dist) * force * 0.02;
                    }
                }
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(${this.baseColor},0.6)`;
                ctx.fill();
            }
        }
        for (let i = 0; i < PARTICLE_COUNT; i++) particles.push(new Particle());
        document.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });
        document.addEventListener('mouseleave', () => { mouse.x = null; mouse.y = null; });

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => { p.update(); p.draw(); });
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    if (dist < CONNECTION_DIST) {
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.strokeStyle = `rgba(6,182,212,${0.15 * (1 - dist/CONNECTION_DIST)})`;
                        ctx.lineWidth = 0.8;
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(animate);
        }
        animate();
    }

    // ─── PAGE NAVIGATION ───
    window.goToPage = function(pageIndex) {
        if (pageIndex < 0 || pageIndex >= state.totalPages || state.isAnimating) return;
        state.isAnimating = true;
        const pages = $$('.page');
        const dots = $$('.page-dots .dot');
        const navLinks = $$('.nav-link');
        const mobileLinks = $$('.mobile-link');

        pages.forEach((p, i) => {
            if (i === pageIndex) {
                p.style.display = 'block';
                p.classList.add('active');
                p.style.animation = 'none';
                p.offsetHeight;
                p.style.animation = 'fadeInUp 0.5s ease-out';
            } else {
                p.classList.remove('active');
                setTimeout(() => { if (!p.classList.contains('active')) p.style.display = 'none'; }, 400);
            }
        });
        dots.forEach((d, i) => d.classList.toggle('active', i === pageIndex));
        navLinks.forEach((l, i) => l.classList.toggle('active', i === pageIndex));
        mobileLinks.forEach((l, i) => l.classList.toggle('active', i === pageIndex));
        state.currentPage = pageIndex;
        updateNavButtons();
        window.scrollTo({ top: 0, behavior: 'smooth' });
        if (pageIndex === 4) setTimeout(initCharts, 300);
        setTimeout(() => { state.isAnimating = false; }, 500);
    };

    function updateNavButtons() {
        const prev = $('#prevPage');
        const next = $('#nextPage');
        if (prev) prev.disabled = state.currentPage === 0;
        if (next) next.disabled = state.currentPage === state.totalPages - 1;
    }

    function initPageNav() {
        $('#prevPage')?.addEventListener('click', () => goToPage(state.currentPage - 1));
        $('#nextPage')?.addEventListener('click', () => goToPage(state.currentPage + 1));
        $$('.page-dots .dot').forEach((dot, i) => dot.addEventListener('click', () => goToPage(i)));
        $$('.nav-link, .mobile-link').forEach((link) => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                goToPage(parseInt(link.dataset.page));
                $('#mobileMenu')?.classList.remove('open');
                $('#hamburger')?.classList.remove('active');
            });
        });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight') goToPage(state.currentPage + 1);
            if (e.key === 'ArrowLeft') goToPage(state.currentPage - 1);
        });
        let touchStartX = 0;
        document.addEventListener('touchstart', (e) => { touchStartX = e.changedTouches[0].screenX; });
        document.addEventListener('touchend', (e) => {
            const diff = touchStartX - e.changedTouches[0].screenX;
            if (Math.abs(diff) > 50) {
                if (diff > 0) goToPage(state.currentPage + 1);
                else goToPage(state.currentPage - 1);
            }
        });
    }

    // ─── MOBILE MENU ───
    function initMobileMenu() {
        const hamburger = $('#hamburger');
        const menu = $('#mobileMenu');
        if (!hamburger || !menu) return;
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            menu.classList.toggle('open');
        });
    }

    // ─── NAV SCROLL ───
    function initNavScroll() {
        const nav = $('#mainNav');
        if (!nav) return;
        window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 20));
    }

    // ─── HERO COUNTERS ───
    function initCounters() {
        const counters = $$('.stat-num[data-target]');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.dataset.target);
                    const suffix = el.textContent.includes('%') ? '%' : (target > 100 ? '+' : '');
                    let current = 0;
                    const increment = target / 60;
                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= target) { current = target; clearInterval(timer); }
                        el.textContent = Math.floor(current) + suffix;
                    }, 25);
                    observer.unobserve(el);
                }
            });
        }, { threshold: 0.5 });
        counters.forEach(c => observer.observe(c));
    }

    // ─── SCROLL REVEAL ───
    function initScrollReveal() {
        const reveals = $$('.feature-card, .model-card, .metric-card, .info-card');
        reveals.forEach(el => el.classList.add('reveal'));
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => entry.target.classList.add('visible'), index * 80);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
        reveals.forEach(el => observer.observe(el));
    }

    // ─── TILT EFFECT ───
    function initTilt() {
        if (window.matchMedia('(pointer: coarse)').matches) return;
        $$('[data-tilt]').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = (y - centerY) / 15;
                const rotateY = (centerX - x) / 15;
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px) scale(1.01)`;
            });
            card.addEventListener('mouseleave', () => { card.style.transform = ''; });
        });
    }

    // ─── DEMO — FAKE NEWS DETECTION SIMULATION ───
    const POSITIVE_WORDS = new Set(['good','great','excellent','amazing','wonderful','fantastic','best','love','happy','positive','success','win','victory','boost','growth','improve','benefit','effective','strong','secure','safe','trust','honest','true','real','genuine','verified','confirmed','approved','support','help','care','progress','advance','achieve','celebrate','proud','honor','respect','peace','stable','prosper','thrive','recommend','praise','commend','outstanding','remarkable','superb','breakthrough','innovation','solution','recovery','optimistic','study','research','data','analysis','report','official','expert','scientist','peer-reviewed','journal','university','institute','survey','statistics','findings','evidence','documented']);
    const NEGATIVE_WORDS = new Set(['bad','terrible','awful','horrible','worst','hate','angry','sad','negative','fail','loss','defeat','crisis','disaster','tragedy','danger','threat','risk','fear','panic','worry','concern','alarm','shocking','exposed','scandal','corrupt','fraud','lie','fake','hoax','conspiracy','secret','hidden','cover','ban','destroy','attack','kill','death','violence','war','conflict','enemy','blame','accuse','guilty','shame','disgrace','outrage','furious','urgent','warning','alert','beware','devastating']);
    const SENSATIONAL_WORDS = new Set(['shocking','breaking','urgent','alert','exposed','revealed','hidden','secret','conspiracy','miracle','cure']);
    const INTENSIFIERS = new Set(['very','extremely','incredibly','absolutely','totally','completely','utterly','highly','deeply','strongly','seriously','severely','especially','particularly','remarkably','exceptionally','most']);

    function analyzeText(text) {
        const words = text.toLowerCase().split(/\s+/);
        const cleanWords = words.map(w => w.replace(/[^a-z]/g, '')).filter(w => w.length > 0);
        if (cleanWords.length === 0) return null;
        let pos = 0, neg = 0, sens = 0, subjWords = 0;
        let capsCount = 0, exclCount = 0, questCount = 0, allCapsWords = 0;
        for (let i = 0; i < words.length; i++) {
            const w = words[i];
            const cw = w.replace(/[^a-z]/g, '');
            if (cw.length === 0) continue;
            if (w === w.toUpperCase() && w.length > 2) allCapsWords++;
            if (POSITIVE_WORDS.has(cw)) { pos++; subjWords++; }
            if (NEGATIVE_WORDS.has(cw)) { neg++; subjWords++; }
            if (INTENSIFIERS.has(cw)) {
                if (i + 1 < words.length) {
                    const next = words[i+1].replace(/[^a-z]/g, '');
                    if (NEGATIVE_WORDS.has(next)) neg += 0.5;
                    if (POSITIVE_WORDS.has(next)) pos += 0.5;
                }
            }
        }
        for (const sw of SENSATIONAL_WORDS) { if (text.toLowerCase().includes(sw)) sens++; }
        for (const c of text) {
            if (c >= 'A' && c <= 'Z') capsCount++;
            if (c === '!') exclCount++;
            if (c === '?') questCount++;
        }
        const total = pos + neg || 1;
        const polarity = (pos - neg) / total;
        const subjectivity = Math.min(1, subjWords / Math.max(cleanWords.length, 1));
        const capsRatio = capsCount / Math.max(text.length, 1);
        const uniqueWords = new Set(cleanWords).size;
        const lexicalDiversity = uniqueWords / Math.max(cleanWords.length, 1);
        const urlCount = (text.match(/http[s]?:\/\/|www\./g) || []).length;
        let fakeScore = 0;
        if (sens >= 2) fakeScore += 30;
        else if (sens >= 1) fakeScore += 15;
        if (subjectivity > 0.5) fakeScore += 20;
        if (capsRatio > 0.1) fakeScore += 15;
        if (allCapsWords >= 2) fakeScore += 10;
        if (exclCount >= 2) fakeScore += 10;
        if (polarity < -0.3) fakeScore += 10;
        if (lexicalDiversity < 0.5 && cleanWords.length > 10) fakeScore += 10;
        if (urlCount === 0 && cleanWords.length > 20) fakeScore += 5;
        if (neg > pos * 1.5) fakeScore += 15;
        if (text.toLowerCase().includes('breaking') || text.toLowerCase().includes('shocking')) fakeScore += 10;
        fakeScore = Math.min(100, Math.max(0, fakeScore));
        return {
            polarity: polarity.toFixed(3),
            subjectivity: subjectivity.toFixed(3),
            wordCount: cleanWords.length,
            sentenceCount: Math.max(1, (text.match(/[.!?]/g) || []).length),
            avgWordLength: (cleanWords.reduce((a,b) => a + b.length, 0) / Math.max(cleanWords.length, 1)).toFixed(2),
            exclamationCount: exclCount,
            questionCount: questCount,
            capsRatio: capsRatio.toFixed(4),
            sensationalScore: sens,
            lexicalDiversity: lexicalDiversity.toFixed(4),
            allCapsWords: allCapsWords,
            urlCount: urlCount,
            fakeScore: fakeScore,
            isFake: fakeScore > 50,
            posWords: pos,
            negWords: neg
        };
    }

    function getModelPredictions(isFake, confidence) {
        const models = [
            { name: 'Logistic Regression', bias: 0.02 },
            { name: 'Random Forest', bias: -0.03 },
            { name: 'Support Vector Machine', bias: 0.01 },
            { name: 'Gradient Boosting', bias: -0.01 }
        ];
        return models.map(m => {
            const adj = confidence + m.bias + (Math.random() * 0.06 - 0.03);
            const pred = adj > 0.5 ? 1 : 0;
            const conf = pred === 1 ? adj : (1 - adj);
            return { ...m, prediction: pred, confidence: Math.min(0.99, Math.max(0.55, conf)) };
        });
    }

    function renderResults(analysis) {
        const container = $('#demoResults');
        if (!container || !analysis) return;
        const models = getModelPredictions(analysis.isFake, analysis.fakeScore / 100);
        const fakeVotes = models.filter(m => m.prediction === 1).length;
        const realVotes = models.length - fakeVotes;
        const consensus = fakeVotes > realVotes ? 'FAKE' : 'GENUINE';
        const consensusColor = consensus === 'FAKE' ? 'fake' : 'real';
        const consensusModels = models.filter(m => m.prediction === (consensus === 'FAKE' ? 1 : 0));
        const avgConf = consensusModels.reduce((a, m) => a + m.confidence, 0) / Math.max(consensusModels.length, 1);
        let riskLevel = 'LOW', riskClass = 'low';
        if (consensus === 'FAKE') {
            if (avgConf > 0.85) { riskLevel = 'CRITICAL'; riskClass = 'critical'; }
            else if (avgConf > 0.60) { riskLevel = 'HIGH'; riskClass = 'high'; }
            else { riskLevel = 'MODERATE'; riskClass = 'moderate'; }
        }
        const featureRows = [
            { label: 'Polarity', value: analysis.polarity, valClass: analysis.polarity < -0.1 ? 'danger' : (analysis.polarity > 0.1 ? 'good' : '') },
            { label: 'Subjectivity', value: analysis.subjectivity, valClass: analysis.subjectivity > 0.5 ? 'warn' : '' },
            { label: 'Word Count', value: analysis.wordCount },
            { label: 'Sensational', value: analysis.sensationalScore, valClass: analysis.sensationalScore >= 2 ? 'danger' : (analysis.sensationalScore >= 1 ? 'warn' : '') },
            { label: 'Caps Ratio', value: (analysis.capsRatio * 100).toFixed(1) + '%', valClass: analysis.capsRatio > 0.1 ? 'warn' : '' },
            { label: 'Lexical Diversity', value: analysis.lexicalDiversity, valClass: analysis.lexicalDiversity < 0.5 ? 'warn' : 'good' },
            { label: 'All-Caps Words', value: analysis.allCapsWords, valClass: analysis.allCapsWords >= 2 ? 'warn' : '' },
            { label: 'URLs Found', value: analysis.urlCount, valClass: analysis.urlCount === 0 ? 'warn' : '' },
        ];
        container.innerHTML = `
            <div class="result-panel glass-card-strong">
                <div class="result-header">
                    <div class="result-verdict ${consensusColor}">${consensus} NEWS ${consensus === 'FAKE' ? '⚠️' : '✅'}</div>
                    <div class="result-confidence ${consensusColor}">${(avgConf * 100).toFixed(1)}%</div>
                </div>
                <div class="result-models">
                    ${models.map(m => `
                        <div class="rmodel-row">
                            <span class="rmodel-name">${m.name}</span>
                            <div class="rmodel-bar-wrap"><div class="rmodel-bar-fill ${m.prediction === 1 ? 'fake' : 'real'}" style="width:${(m.confidence * 100).toFixed(0)}%"></div></div>
                            <span class="rmodel-pct ${m.prediction === 1 ? 'danger' : 'good'}">${(m.confidence * 100).toFixed(0)}%</span>
                        </div>
                    `).join('')}
                </div>
                <div style="margin-bottom:12px;font-size:0.85rem;color:var(--text-muted);text-align:center;">
                    Ensemble: ${fakeVotes} Fake vs ${realVotes} Real votes
                </div>
                <div class="result-features">
                    ${featureRows.map(f => `
                        <div class="rfeat-item">
                            <span class="rfeat-label">${f.label}</span>
                            <span class="rfeat-val ${f.valClass || ''}">${f.value}</span>
                        </div>
                    `).join('')}
                </div>
                <div class="result-risk ${riskClass}">Risk: ${riskLevel}</div>
            </div>
        `;
    }

    function initDemo() {
        const analyzeBtn = $('#analyzeBtn');
        const clearBtn = $('#clearBtn');
        const demoText = $('#demoText');
        const tabs = $$('.demo-tab');
        const tabContents = $$('.demo-tab-content');
        const sampleItems = $$('.sample-item');
        if (!analyzeBtn) return;

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));
                tab.classList.add('active');
                const target = $('#tab-' + tab.dataset.tab);
                if (target) target.classList.add('active');
            });
        });

        sampleItems.forEach(item => {
            item.addEventListener('click', () => {
                if (demoText) demoText.value = item.dataset.text || '';
                tabs.forEach(t => t.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));
                if (tabs[0]) tabs[0].classList.add('active');
                const target = $('#tab-paste');
                if (target) target.classList.add('active');
            });
        });

        analyzeBtn.addEventListener('click', () => {
            const text = demoText?.value?.trim();
            if (!text) { alert('Please enter some text to analyze!'); return; }
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = '<span style="display:inline-block;width:16px;height:16px;border:2px solid rgba(255,255,255,0.3);border-top-color:white;border-radius:50%;animation:spin 0.8s linear infinite;"></span><span>Analyzing...</span>';
            setTimeout(() => {
                const result = analyzeText(text);
                renderResults(result);
                analyzeBtn.disabled = false;
                analyzeBtn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg><span>Analyze Article</span>`;
            }, 800);
        });

        clearBtn?.addEventListener('click', () => {
            if (demoText) demoText.value = '';
            const results = $('#demoResults');
            if (results) results.innerHTML = `
                <div class="results-placeholder">
                    <div class="rp-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><path d="M9 12h6M12 9v6M12 2a10 10 0 100 20 10 10 0 000-20z"/></svg></div>
                    <p>Enter text and click Analyze to see results</p>
                </div>
            `;
        });
    }

    // ─── CHARTS (Chart.js) ───
    function initCharts() {
        if (!window.Chart) return;
        const commonOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#94a3b8', font: { family: 'Inter', size: 11 } } }
            },
            scales: {
                x: { ticks: { color: '#64748b', font: { family: 'Inter', size: 10 } }, grid: { color: 'rgba(148,163,184,0.08)' } },
                y: { ticks: { color: '#64748b', font: { family: 'Inter', size: 10 } }, grid: { color: 'rgba(148,163,184,0.08)' }, beginAtZero: true, max: 1 }
            }
        };

        // Accuracy Chart
        const accCtx = $('#chartAccuracy')?.getContext('2d');
        if (accCtx && !state.charts.accuracy) {
            state.charts.accuracy = new Chart(accCtx, {
                type: 'bar',
                data: {
                    labels: ['Logistic Regression', 'Random Forest', 'SVM', 'Gradient Boosting'],
                    datasets: [
                        { label: 'Test Accuracy', data: [0.921, 0.958, 0.937, 0.975], backgroundColor: 'rgba(6,182,212,0.7)', borderColor: '#06b6d4', borderWidth: 1, borderRadius: 6 },
                        { label: 'CV Accuracy', data: [0.894, 0.932, 0.911, 0.958], backgroundColor: 'rgba(139,92,246,0.6)', borderColor: '#8b5cf6', borderWidth: 1, borderRadius: 6 }
                    ]
                },
                options: { ...commonOptions, scales: { ...commonOptions.scales, y: { ...commonOptions.scales.y, max: 1.1 } } }
            });
        }

        // ROC Chart
        const rocCtx = $('#chartRoc')?.getContext('2d');
        if (rocCtx && !state.charts.roc) {
            state.charts.roc = new Chart(rocCtx, {
                type: 'line',
                data: {
                    labels: ['0.0', '0.2', '0.4', '0.6', '0.8', '1.0'],
                    datasets: [
                        { label: 'LogReg (0.941)', data: [0, 0.72, 0.85, 0.92, 0.97, 1], borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,0.1)', tension: 0.4, fill: true, pointRadius: 3 },
                        { label: 'RF (0.978)', data: [0, 0.78, 0.90, 0.95, 0.98, 1], borderColor: '#10b981', backgroundColor: 'rgba(16,185,129,0.1)', tension: 0.4, fill: true, pointRadius: 3 },
                        { label: 'SVM (0.953)', data: [0, 0.74, 0.87, 0.93, 0.96, 1], borderColor: '#f59e0b', backgroundColor: 'rgba(245,158,11,0.1)', tension: 0.4, fill: true, pointRadius: 3 },
                        { label: 'GB (0.989)', data: [0, 0.82, 0.93, 0.97, 0.99, 1], borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,0.1)', tension: 0.4, fill: true, pointRadius: 3 },
                        { label: 'Baseline', data: [0, 0.2, 0.4, 0.6, 0.8, 1], borderColor: '#64748b', borderDash: [5,5], tension: 0, pointRadius: 0, fill: false }
                    ]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: '#94a3b8', font: { family: 'Inter', size: 10 }, boxWidth: 12 } } },
                    scales: {
                        x: { title: { display: true, text: 'False Positive Rate', color: '#64748b', font: { size: 10 } }, ticks: { color: '#64748b' }, grid: { color: 'rgba(148,163,184,0.08)' } },
                        y: { title: { display: true, text: 'True Positive Rate', color: '#64748b', font: { size: 10 } }, ticks: { color: '#64748b' }, grid: { color: 'rgba(148,163,184,0.08)' }, beginAtZero: true, max: 1 }
                    }
                }
            });
        }

        // Training Time Chart
        const timeCtx = $('#chartTime')?.getContext('2d');
        if (timeCtx && !state.charts.time) {
            state.charts.time = new Chart(timeCtx, {
                type: 'doughnut',
                data: {
                    labels: ['LogReg', 'Random Forest', 'SVM', 'GradBoost'],
                    datasets: [{
                        data: [0.45, 2.8, 1.2, 3.5],
                        backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
                        borderColor: '#1e293b', borderWidth: 2
                    }]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right', labels: { color: '#94a3b8', font: { family: 'Inter', size: 10 }, boxWidth: 12 } }
                    },
                    cutout: '65%'
                }
            });
        }
    }

    // ─── INIT ───
    function init() {
        initCursor();
        initCanvas();
        initPageNav();
        initMobileMenu();
        initNavScroll();
        initCounters();
        initScrollReveal();
        initTilt();
        initDemo();
        updateNavButtons();
        // Ensure only page 0 visible initially
        $$('.page').forEach((p, i) => { p.style.display = i === 0 ? 'block' : 'none'; });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
