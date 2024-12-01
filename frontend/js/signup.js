// ブラウザにトークンが保存されているかを確認する
const token = localStorage.getItem('token');
// 保存されていたらサインアップの必要がないのでタイムラインのページに移動する
if (token !== null) {
    location.href = './home.html';
}

async function submit() {
    // フォームから名前とメールアドレスとパスワードを取得する
    const user_name = document.getElementById('input_name').value;
    const email = document.getElementById('input_email').value;
    const password = document.getElementById('input_pass').value;
    // 上記の情報をAPIサーバに送り、ユーザを登録する
    const tmp_res = await fetch('/api/users/signup', {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
        },
        method: 'POST',
        body: JSON.stringify({
            'name': user_name,
            'email': email,
            'password': password,
        }),
    });
    // 失敗したらalertを出す
    if (tmp_res.status !== 200) {
        alert('signup is failed');
        return;
    }
    // 更にメールアドレスとパスワードをAPIサーバに送りサインインする
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
    data = await response.json();
    localStorage.setItem('token', data.token);
    // タイムラインのページに移動する
    location.href = './home.html';
}
