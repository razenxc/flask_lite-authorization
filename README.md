<h1>flask_lite-authorization</h1>
<p>Web authorization written on the flask library</p>
<h2>Installation</h2>
<ul>
    <li>
        <table>
        <p><a href="https://flask.palletsprojects.com/en/2.3.x/installation/#create-an-environment" style="color:cyan;">Create an environment</a></p>
            <tr>
                <th>Windows</th>
                <th>Linux/macOS</th>
            </tr>
            <tr>
                <th><code>py -3 -m venv .venv</code></th>
                <th><code>python3 -m venv .venv</code></th>
            </tr>
        </table>
    </li>
    <li>
        <table>
            <p><a href="https://flask.palletsprojects.com/en/2.3.x/installation/#activate-the-environment" style="color:cyan;">Activate the environment</a></p>
            <tr>
                <th>Windows</th>
                <th>Linux/macOS</th>
            </tr>
            <tr>
                <th><code>.venv\Scripts\activate</code></th>
                <th><code>. .venv/bin/activate</code></th>
            </tr>
        </table>
    </li>
    <li>Install the Project with <code>pip install -e .</code></li>
    <li>Create <code>.env</code> file in project directory</li>
    <li>Gen secret key with <code>python -c "import secrets; print(secrets.token_hex())"</code> in console/terminal and copy it</li>
    <li>Paste generated secret key in <code>FLASK_SECRET_KEY="paste-here"</code> to <code>.env</code></li>
    <li>Paste db URI in <code>SQLALCHEMY_DB_URI="here"</code> for sqlite use <code>sqlite:///database.sqlite</code></li>
    <li>.env should look like this:<br>
    <code>FLASK_SECRET_KEY="ur_key"</code><br>
    <code>SQLALCHEMY_DB_URI="sqlite:///database.sqlite"</code></li>
</ul>
<h2>Launching</h2>
<ul>
    <li>Development server <code>flask --app liteauth:app run --debug</code></li>
    <li>Production waitress server <code>waitress-serve --host localhost --call liteauth:app</code></li>
    <li>* Also you can use <code>launch.bat</code> if you on windows, enter in your terminal <code>launch</code> and it output launch parameters</li>
</ul>
