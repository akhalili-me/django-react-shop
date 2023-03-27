import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination, Scrollbar, A11y } from "swiper";
// Import Swiper styles
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "swiper/css/scrollbar";

function HomeSwiper() {
  return (
    <Swiper
      // install Swiper modules
      className=""
      modules={[Navigation, Pagination, Scrollbar, A11y]}
      spaceBetween={50}
      slidesPerView={1}
      navigation
      loop
      pagination={{ clickable: true }}
      scrollbar={{ draggable: true }}
    >
      <SwiperSlide>
        <img
          className=""
          alt=""
          src="https://smartslider3.com/wp-content/uploads/2019/05/fullwidthslider.jpg"
        ></img>
      </SwiperSlide>
      <SwiperSlide>
        <img
          className=""
          alt=""
          src="https://unsplash.com/photos/vloKy1It5Mg/download?ixid=MnwxMjA3fDB8MXxzZWFyY2h8M3x8d2lkZXxlbnwwfHx8fDE2NzY5ODM0MDU&force=true"
        ></img>
      </SwiperSlide>
    </Swiper>
  );
}

export default HomeSwiper;
