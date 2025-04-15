<template>
  <section class="hero-section">
    <swiper
      :modules="swiperModules"
      :slides-per-view="1"
      :space-between="0"
      :loop="true"
      :effect="'fade'"
      :fade-effect="{ crossFade: true }"
      :pagination="{ clickable: true }"
      :navigation="true"
      :autoplay="{
        delay: 5000,
        disableOnInteraction: false,
      }"
      @slideChange="onSlideChange" 
      class="hero-swiper"
    >
      <swiper-slide v-for="(slide, index) in slides" :key="index">
        <div class="slide-background">
          <img :src="slide.imageUrl" :alt="slide.altText" class="hero-image" />
        </div>
      </swiper-slide>
    </swiper>

    <!-- 内容覆盖层，现在绑定动态数据 -->
    <div class="hero-content-overlay container">
        <h1>{{ currentTitle }}</h1>
        <p>{{ currentDescription }}</p>
        <!-- <button class="cta-button">探索产品</button> -->
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css/effect-fade';
import { Navigation, Pagination, Autoplay, EffectFade } from 'swiper/modules';

const swiperModules = [Navigation, Pagination, Autoplay, EffectFade];

// 为 slides 添加 title 和 description
const slides = ref([
  {
    imageUrl: '/img/天山雪线下的蜂场.png',
    altText: '天山雪线下的蜂场',
    title: '天山蜜源地 | 自然纯净',
    description: '海拔2000-3688米垂直蜜源带，与冰川为邻，200公里生态隔离区孕育450种蜜源植物'
  },
  {
    imageUrl: '/img/新疆黑蜂采蜜.png',
    altText: '新疆黑蜂采蜜',
    title: '珍稀新疆黑蜂 | 活力充沛',
    description: '中国四大名蜂之一，翼展达12.8mm，零下30℃仍可出巢，单蜂日采蜜量比普通蜂种高37%'
  },
  {
    imageUrl: '/img/手工割蜜过程.png',
    altText: '手工割蜜过程',
    title: '手工割蜜 | 匠心传承',
    description: '遵循自然法则，低温物理过滤，保留每一滴的原生营养。'
  },
  {
    imageUrl: '/img/实验室检测场景1.png',
    altText: '实验室检测场景',
    title: '欧盟检测标准 | 安心之选',
    description: '通过BRC/IFS双认证，216项检测指标超欧盟标准，每瓶蜜可扫码查看重金属检测报告'
  },
  {
    imageUrl: '/img/结晶蜜显微结构.png',
    altText: '结晶蜜显微结构',
    title: '原蜜零添加 | 自然本真味',
    description: '葡萄糖晶体自然析出，每平方厘米超800个结晶核，证明未经过高温破晶处理'
  },
  {
    imageUrl: "/img/天然隔离带中的蜂场.png",
    altText: "天然隔离带中的蜂场",
    title: "百里生态屏障 | 纯净蜜源圈",
    description: "半径150公里无工业区，蜜源植物天然抗病虫，无需农药的纯净生态系统"
  },
  {
    imageUrl: "/img/蜜液透光展示.png",
    altText: "蜜液透光展示",
    title: "晶润琥珀色 | 自然光感蜜",
    description: "含水量17.8%的黄金平衡点，入口5秒即化，留下百种芳香物质"
  },
  {
    imageUrl: "/img/四季结晶对比.png",
    altText: "四季结晶对比",
    title: "四季可结晶 | 纯蜜身份证",
    description: "春夏呈乳酪状，秋冬现鱼籽纹，温度适应性证明无添加的天然特性"
  },
  {
    imageUrl: "/img/晨间取蜜仪式.png",
    altText: "晨间取蜜仪式",
    title: "每日蜜一勺 | 元气补给站",
    description: "含16种氨基酸和7种矿物质，β-葡聚糖含量达2.3mg/100g"
  },
]);

// 用于存储当前显示的文本的响应式变量
// 初始化为第一个 slide 的内容
const currentTitle = ref(slides.value[0].title);
const currentDescription = ref(slides.value[0].description);

// Swiper 切换事件处理函数
const onSlideChange = (swiper) => {
  // swiper.realIndex 在 loop 模式下获取真实的当前幻灯片索引
  const realIndex = swiper.realIndex;
  if (slides.value[realIndex]) {
    currentTitle.value = slides.value[realIndex].title;
    currentDescription.value = slides.value[realIndex].description;
  }
};

</script>

<style scoped>
.hero-section {
  position: relative;
  height: 512px;
  overflow: hidden;
}

.hero-swiper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.slide-background {
  width: 100%;
  height: 100%;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  /* filter: brightness(0.6); */ /* 移除亮度滤镜 */
}

.hero-content-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  color: #fff;
  text-align: center;
  max-width: 800px;
  width: 90%;
}

.hero-content-overlay h1 {
  font-size: 2.8rem;
  margin-bottom: 1rem;
  color: #fff;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.8); /* 加强阴影以确保对比度 */
}

.hero-content-overlay p {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.8); /* 加强阴影 */
}

:deep(.swiper-button-prev),
:deep(.swiper-button-next) {
  color: var(--primary-color);
  --swiper-navigation-size: 30px;
  /* 可以给按钮背景加一点阴影，防止在亮色图片上看不清 */
  filter: drop-shadow(0px 0px 3px rgba(0, 0, 0, 0.5));
}

:deep(.swiper-pagination-bullet) {
  background-color: rgba(255, 255, 255, 0.6);
  width: 12px; /* 稍微增大 */
  height: 12px;
  opacity: 1;
  border: 1px solid rgba(0, 0, 0, 0.2);
}

:deep(.swiper-pagination-bullet-active) {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.cta-button {
  padding: 0.8rem 2rem;
  font-size: 1rem;
  background-color: var(--primary-color);
  color: var(--text-color-dark);
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.cta-button:hover {
  background-color: #ffab6f;
}
</style> 