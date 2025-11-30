---
title: Test-Index
toc: false
---

<div class="hero">
  <h1>Final Project Dashboard</h1>
  <h2>Visual Analysis of Focus, Mood and more!</h2>
  <a href="./dashboard" class="card" 
    style=
      "
       display: block;
       text-decoration: none;
       color: inherit; 
       padding: 2rem; 
       margin-top: 2rem;
       max-width: 400px; 
       border: 1px solid var(--theme-foreground-faint);
      ">
  <h3 style="margin-top: 0; font-weight: 600;">
    Go to Dashboard <span style="display: inline-block; margin-left: 0.25em;">→</span>
  </h3>
  </a>
</div>

<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 8rem;
  text-wrap: balance;
  text-align: center;
  min-height: 80vh;
}

.hero h1 {
  margin: 1rem 0;
  padding: 1rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>
