<template>
  <div class="about-us">
    <div class="about-us-header">
      <h3>Vision/Mission</h3>
      <p>全ての旅行者が笑顔で帰れるように</p>
    </div>

    <p class="about-us-description">
      この旅行、とても良かった。全ての旅行者が帰
      宅して一息ついた時、心からそう思える旅をし
      て欲しい。そんな思いから、サービスを立ち上
      げました。すべての利用者様がいい旅を出来る
    </p>

    <div class="about-us-title">
      会社情報
    </div>

    <div class="about-us-contact">
      <p>
        <label>会社名</label>
        <span>TraveiQA, Inc</span>
      </p>
      <p>
        <label>所在地</label>
        <span>〒103 -0007 東京都中央区</span>
      </p>
      <p>
        <label>設立</label>
        <span>2020年</span>
      </p>
      <p>
        <label>事業内容</label>
        <span>「TraveiQA」の企画運営</span>
      </p>
      <p>
        <label>連絡先</label>
        <span>aaa@aaaa.com</span>
      </p>
    </div>
  </div>
</template>

<style lang="css" scoped>
.about-us-header {
  margin-top: 20px;
  margin-bottom: 30px;
}

.about-us-header h3 {
  font-size: 18px;
  color: #235fbb;
  font-weight: 600;
  margin-bottom: 0;
}

.about-us-header p {
  font-size: 22px;
  font-weight: 600;
}

.about-us-description {
  margin-bottom: 20px;
}

.about-us-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 20px;
}

.about-us-contact {
  text-align: left;
  font-size: 14px;
  width: 350px;
  margin: 0 auto;
}

.about-us-contact p {
  margin-bottom: -5px;
}

.about-us-contact label {
  width: 100px;
  font-weight: 600;
}

@media only screen and (max-width: 600px) {
  .about-us-contact {
    width: 100%;
  }

  .about-us-contact label {
    width: 70px;
    font-weight: 600;
  }
}
</style>
