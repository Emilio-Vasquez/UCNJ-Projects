function throwConfetti() {
  try {
    if (typeof confetti === 'function') {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
    } else {
  
    }
  } catch (e) {
    console.warn('confetti error:', e);
  }
}
