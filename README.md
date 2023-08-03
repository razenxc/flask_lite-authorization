<h1>flask_lite-authorization</h1>
<p>Web authorization written on the flask library</p>
<h2>Installation</h2>
<ul>
    <li><code>pip install -r requirements.txt</code></li>
    <li>Create <code>.env</code> file in project directory</li>
    <li>Gen secret key with <code>python -c "import secrets; print(secrets.token_hex())"</code> in console/terminal and copy it</li>
    <li>Paste generated secret key in <code>FLASK_SECRET_KEY="paste-here"</code> to <code>.env</code></li>
</ul>
<h2>Laucnhing</h2>
<ul>
    <li>Development server <code>flask --app liteauth:app run --debug</code></li>
    <li>Production waitress server <code>waitress-serve --host localhost --call liteauth:app</code></li>
</ul>