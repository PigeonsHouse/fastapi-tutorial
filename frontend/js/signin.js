// ブラウザにトークンが保存されているかを確認する
const token = localStorage.getItem('token');
// 保存されていたらサインアップの必要がないのでタイムラインのページに移動する
if (token !== null) {
    location.href = './home.html';
}

async function submit() {
    // フォームからメールアドレスとパスワードを取得する
    const email = document.getElementById('input_email').value;
    const password = document.getElementById('input_pass').value;
    // メールアドレスとパスワードをAPIサーバに送りサインインする
    const response = await fetch('/api/users/signin', {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
        },
        method: 'POST',
        body: JSON.stringify({
            'email': email,
            'password': password,
        }),
    });
    // 失敗したらalertを出す
    if (response.status !== 200) {
        alert('signin is failed');
        return;
    }
    // 成功したら、APIが返すトークンをブラウザに保存する
    const data = await response.json();
    localStorage.setItem('token', data.token);
    // タイムラインのページに移動する
    location.href = './home.html';
}
