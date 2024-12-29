<div class="text-xl">
  <span v-after v-mark.underline.blue="2">Sandboxing </span>
  <span v-after v-mark.underline.orange="1">Agentic Workflows</span>
  with
  <span v-after v-mark.underline.green="3">WASM</span>
</div>

Joe Lucas
---
layout: default
---

## Agentic Workflows

<div v-click>1. LLMs can generate code</div>
<div v-click>2. Copy and paste is lame</div>
<div v-click>3. Why don't we just <code>exec()/eval()</code> it?</div>

---
layout: default
---

## _You_ Knew it was a Terrible Idea

<div class="relative">
  <img 
    v-click="2"
    src="/static/exec.png"
    class="absolute top-0 left-0"
  />
  <img 
    v-click="3"
    src="/static/regex.png"
    class="absolute top-0 left-0"
  />
</div>

<div v-after>Between them, these libraries have almost 30k stars on GitHub.</div>

---
layout: default
---

## A note on LLMs

Treat LLM-generated code as untrusted
<div v-click>especially when it's operating with user/external input</div>

---
layout: default
---

## Agentic Workflows (Example)

<div v-click>We want to create data visualizations for our users.</div>
<div v-click>We can prompt an LLM to give us this code.</div>
<div v-click>
```python {monaco}
fig = go.Figure(data=go.Scatter(
  x=[1, 2, 3], 
  y=[1, 2, 3]))
fig.update_layout(title='Test Plot')
```
</div>
<div v-click>Now what?</div>

---
layout: default
---

## Sandboxes

<div v-click>- VMs are hard</div>
<div v-click>- Containers aren't security boundaries</div>
<div v-click>- What about browsers?</div>

---
layout: default
---

## Yeeting Python from Server to Client

Remember that our prompting strategy gave us this:

```python {monaco}
fig = go.Figure(data=go.Scatter(
  x=[1, 2, 3], 
  y=[1, 2, 3]))
fig.update_layout(title='Test Plot')
```

<div v-click>We can template that straight into our HTML!</div>

---
layout: default
---

## Sticking It All Together

````md magic-move {lines: true}
```js {*|4-5}
async function initPyodide() {
    try {
        let pyodide = await loadPyodide();
        await pyodide.loadPackage("micropip");
        await micropip.install('plotly');
        return pyodide;
    } catch (error) { throw error; }
}
```

```js {*|4-5|7,17}
window.runCode = async (userCode) => {
    const pyodide = await initPyodide();
    const wrappedCode = [
        'import plotly.graph_objects as go',
        'import json',
        'try:',
        '    ' + userCode.replace(/\n/g, '\n    '),
        '    if "fig" in locals():',
        '        plotJson = fig.to_json()',
        '    else:',
        '        raise Exception("No fig variable found")',
        'except Exception as e:',
        '    print(f"Python execution error: {str(e)}")',
        '    raise'
    ].join('\n');
    const svg = await Plotly.toImage('plot', {format: 'svg'});
    return svg;
}
```

```js {*|1|16-19}
app.post('/execute', async (req, res) => {
    const { code } = req.body;
    if (!code) {
        return res.status(400).send('No code provided');
    }
    let page;
    try {
        const context = await browser.newContext({
            javaScriptEnabled: true,
            permissions: []
        });
        
        page = await context.newPage();
        await page.setContent(HTML_TEMPLATE);

        const svg = await page.evaluate(async (code) => {
            return await window.runCode(code);
        }, code);
        res.send({ svg });
    }
```
````

---
layout: end
---

## Thank You

Code: `https://github.com/JosephTLucas/wasm-plotly`

bsky: `@hackthis.ai`