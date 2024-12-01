// ブラウザに保存されているトークンを取得する
const token = localStorage.getItem('token');
// 保存されていなかったらサインアップの必要があるのでトップページに移動する
if (token === null) {
    location.href = '/';
}
// 保存されているトークンが有効か確認するため自分の情報を取得する
const response = await fetch('/api/users/me', {
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': `Bearer ${token}`,
    },
});
// 取得に失敗したらトークンが無効ということになる
if (response.status !== 200) {
    // alertを出し、ブラウザから無効なトークンを削除して、トップページに移動する
    alert('authentication is failed');
    localStorage.removeItem('token');
    location.href = '/';
}

// 取得に成功した自身の情報を表示する
const user = await response.json();
document.getElementById('display_name').innerHTML = `ユーザー名：${user.name}`;

// タイムラインに表示する投稿一覧を取得する
const timeline_response = await fetch('/api/contents', {
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': `Bearer ${token}`,
    },
});
// 取得に失敗したらalertを出す
if (timeline_response.status != 200) {
    alert('getting content is failed');
} else {
    const timelines = await timeline_response.json();

    timelines.map((content) =>
        document.getElementById('timeline')
            .insertAdjacentHTML('beforeend', createContentStr(content.user.name, content.content, content.created_at))
    )
}
