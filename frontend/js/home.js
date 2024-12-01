// ブラウザにトークンが保存されているかを確認する
const token = localStorage.getItem('token');
// 保存されていなかったらサインアップの必要があるのでトップページに移動する
if (token === null) {
    location.href = '/';
}

// タイムラインの投稿一つ分のHTMLを返す関数
function createContentStr(user_name, content, time) {
    return `
    <div class="content">
        <br/>
        <span>
            <b>${user_name}</b>
        </span>
        <p>${content}</p>
        <small>${time}</small>
    </div>
    <br/>
    <hr>
    `;
}

async function submitContent() {
    // 投稿フォームから文章を取得
    const content = document.getElementById('content').value;
    // トークンと共に文章をAPIサーバに送り、投稿を保存してもらう
    await fetch('/api/contents', {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': `Bearer ${token}`,
        },
        method: 'POST',
        body: JSON.stringify({
            'content': content,
        }),
    });
    // タイムラインページに移動する(=リロードの代わり)
    location.href = './home.html';
}

function logout() {
    // ブラウザからトークンを削除して、トップページに移動する
    localStorage.removeItem('token');
    location.href = '/';
}
