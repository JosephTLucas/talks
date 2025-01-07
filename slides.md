---
layout: cover
---

<div class="text-center text-xl">
  <span v-after v-mark.underline.blue="2">Sandboxing </span>
  <span v-after v-mark.underline.orange="1">Agentic Workflows</span>
  with
  <span v-after v-mark.underline.green="3">WASM</span>
</div>

<div class="text-center mt-4 text-small">
Joe Lucas
</div>
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

<div v-click>
```python {monaco}
def check_malicious_keywords_in_query(self, query):
  dangerous_pattern = re.compile(
    r"\b(os|io|chr|b64decode)\b|"
    r"(\.os|\.io|'os'|'io'|\"os\"|\"io\"|chr\(|chr\)|chr |\(chr)"
```
</div>

<div v-click>
```python {monaco}
try:
  exec(plotly_code, globals(), ldict)
  fig = ldict.get("fig", None)
```
</div>

<div v-click>Between them, these libraries have almost 30k stars on GitHub.</div>

<CitationList :citations="[
'https://github.com/Sinaptik-AI/pandas-ai/blob/cf33faa5de1fd6ae565240b8eb4373f5de7c929f/pandasai/agent/base.py#L237',
'https://github.com/vanna-ai/vanna/blob/ad014c44a4bf5bd15ffb576ffd85578ad17e1a2f/src/vanna/base/base.py#L2146'
]":clickIndex="[1, 2]" />
---
layout: default
---

## A note on LLMs

Treat LLM-generated code as untrusted <span v-click>especially when it's operating with user/external input.</span>
<br><br>
<div v-click><i>The AI bit of this talk was just clickbait. We're really just talking about sandboxing untrusted code.</i></div> <span v-click>sorry... but that's the state of appsec for some of these applications.</span>

---
layout: default
---

## Agentic Workflows (Example)

<div v-click>We want to create data visualizations for our users.</div>
<div v-click>We can prompt an LLM to give us this code. 🪄</div>
<div v-click>
```python {monaco}
fig = go.Figure(data=go.Scatter(
  x=[1, 2, 3], 
  y=[1, 2, 3]))
fig.update_layout(title='Test Plot')
```
</div>
<div v-click><i>Now what?</i></div>

---
layout: default
---

## Sandboxes

<div v-click>- VMs are hard, but use them if you can [1]</div>
<div v-click>- Containers aren't security boundaries [2]</div>
<div v-click>- What about browsers?</div>

<CitationList :citations="[
'🤗 smolagents uses microvms through e2b.dev', 
'This was an interview question for SecEng at AWS'
]":clickIndex="[1, 2]" />

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
layout: default
---
## Demo
Here's a demo

---
layout: two-cols
---
## What did we gain?
<div v-click>- Isolation from bad users</div>
<div v-click>- Isolating users from bad neighbors</div>
<div v-click>- Reduced compute requirements</div>
<div v-click>- Data localization</div>

::right::
## What did we lose?
<div v-click>- Speed (maybe)</div>
<div v-click>- Service-side integrations</div>
<div v-click>- Data localization</div>

---
layout: default
---
## Considerations

<div v-click>- Security vs Dev Speed vs UX... just as it ever was</div>
<div v-click>- Some dependencies are easier to work with, but you can ship your own wheels [1]</div>
<div v-click>- Pyodide is just one way to do this, plenty of other languages support wasm as a target</div>
<div v-click>- 📈 wasm AI stuff [2][3]</div>

<CitationList :citations="[
'https://pyodide.org/en/stable/usage/loading-packages.html#installing-wheels-from-arbitrary-urls',
'https://www.mcp.run/',
'https://simonwillison.net/2024/Dec/10/chatgpt-canvas/'
]":clickIndex="[2, 4, 4]" />

---
layout: end
---

## Thank You

Code: `https://github.com/JosephTLucas/wasm-plotly`

bsky: `@hackthis.ai`

More: `https://developer.nvidia.com/blog/tag/ai-red-team/`