// ブラウザにトークンが保存されているかを確認する
const token = localStorage.getItem('token');
// 保存されていたらサインアップの必要がないのでタイムラインのページに移動する
if (token !== null) {
    location.href = './home.html';
}
