<template>
  <div class="new-registe">
    <div class="new-registe-header">
      <h3>TraveiQA</h3>
      <p>あなたにあつた旅が見つかるQAサイト</p>
    </div>

    <p class="new-registe-description">
      TraveiQAは旅行に関するQAサーヒスぐす。ホテル選びか
      らお店探しまで、様々な悩みを質問することが出来ます．
      投稿《ま全て無料で見ることができます！
    </p>

    <div class="new-registe-title">
      会社情報
    </div>

    <div class="new-registe-form">
      <div class="new-registe-form-item custom-form-item">
        <div>
          <label>aaa</label>
          <input type="text" class="new-registe-form-input" />
        </div>

        <div>
          <label>bbb</label>
          <input type="text" class="new-registe-form-input" />
        </div>
      </div>

      <div class="new-registe-form-item">
        <label>メー）レアドレス </label>
        <input type="text" class="new-registe-form-input" />
      </div>

      <div class="new-registe-form-item">
        <label>ノ（スワード </label>
        <input type="text" class="new-registe-form-input" />
      </div>

      <div class="new-registe-form-descriptions">
        「新規登録」をクリックすることで、TraveiQA
      </div>
      <div class="new-registe-form-descriptions">
        の<span>利用規約</span>と<span>プライパシーポリシー</span>を証んで「司
      </div>
      <div class="new-registe-form-descriptions text-right">
        <span>キャン飢</span> &nbsp;&nbsp;
        <button class="btn btn-primary">C露D キャ</button>
      </div>
    </div>
  </div>
</template>

<style lang="css" scoped>
.new-registe {
  padding: 80px 30px 30px 30px;
}
.new-registe-header h3 {
  font-size: 35px;
  color: #235fbb;
  font-weight: 600;
}

.new-registe-header p {
  font-size: 22px;
  font-weight: 600;
}

.new-registe-description {
  margin-bottom: 20px;
  color: #727272;
}

.new-registe-title {
  margin-bottom: 10px;
  color: #727272;
}

.new-registe-form {
  padding: 0 15px;
  color: #202020;
  max-width: 500px;
  margin: 0 auto;
}

.new-registe-form-item {
  margin-bottom: 10px;
  padding: 0 10px;
}

.new-registe-form-item label {
  display: block;
  margin-bottom: 0;
  text-align: left;
  font-size: 14px;
}

.new-registe-form-input {
  width: 100%;
  border: 1px solid #707070;
  padding-left: 15px;
  padding-right: 15px;
}

.custom-form-item {
  display: flex;
  justify-content: space-between;
}

.custom-form-item div {
  width: 45%;
}

.new-registe-form-descriptions {
  font-size: 14px;
  margin-bottom: 5px;
}

.new-registe-form-descriptions span {
  color: #4569b3;
}

.text-right {
  margin-top: 5px;
}

.btn-primary {
  padding: 2px 5px;
  border-radius: 20px;
  background-color: #2761e6;
  border: 1px solid #707070;
}
@media only screen and (max-width: 600px) {
  .new-registe-form {
    max-width: 100%;
  }
}
</style>
