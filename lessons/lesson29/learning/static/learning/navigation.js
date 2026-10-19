function translateNavigation() {
    const lang = localStorage.getItem('lesson29-language') === 'en' ? 'en' :
        'pl';
    document.querySelectorAll('[data-pl]').forEach(node => node.textContent =
        node.dataset[lang]);
    document.documentElement.lang = lang;
    for (const value of ['pl', 'en']) {
        const button = document.getElementById(value);
        button?.classList.toggle('active', lang === value);
    }
    if (document.body.classList.contains('catalog-body')) document.title =
        `Celery Lab · ${lang==='pl'?'Zadania':'Tasks'}`;
}
if (document.body.classList.contains('catalog-body'))
    for (const lang of ['pl', 'en']) document.getElementById(lang).onclick =
    () => {
            localStorage.setItem('lesson29-language', lang);
            translateNavigation();
        };
const rail = document.getElementById('task-rail');
if (rail) {
    const toggle = document.getElementById('task-list-toggle'),
        drawer = document.getElementById('task-drawer');
    let pinned = false;

    function setOpen(open) {
        rail.classList.toggle('is-open', open);
        toggle.setAttribute('aria-expanded', open);
        drawer.inert = !open;
    }
    rail.addEventListener('mouseenter', () => setOpen(true));
    rail.addEventListener('mouseleave', () => {
        if (!pinned && !drawer.contains(document.activeElement))
            setOpen(false);
    });
    toggle.onclick = () => {
        pinned = !pinned;
        setOpen(pinned);
    };
    document.getElementById('task-list-close').onclick = () => {
        pinned = false;
        toggle.focus();
        setOpen(false);
    };
    rail.addEventListener('keydown', event => {
        if (event.key === 'Escape') {
            pinned = false;
            toggle.focus();
            setOpen(false);
        }
    });
    document.addEventListener('pointerdown', event => {
        if (!rail.contains(event.target)) {
            pinned = false;
            setOpen(false);
        }
    });
    rail.addEventListener('focusout', () => {
        setTimeout(() => {
            if (!pinned && !rail.contains(document
                    .activeElement)) setOpen(false);
        }, 0);
    });
}
translateNavigation();
