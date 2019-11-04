
/**
 * Countdown
 */
function init() {
    const second = 1000,
          minute = second * 60,
          hour   = minute * 60,
          day    = hour * 24;
  
    const date = document.querySelector('[data-date]').dataset.date;
  
    let countDown = new Date(date).getTime(),
      x = setInterval(function () {
  
        let now = new Date().getTime(),
            distance = countDown - now;
  
        if (document.querySelector('[data-days]') != null) {
          document.querySelector('[data-days]').innerText = Math.floor(distance / (day));
        }
  
        if (document.querySelector('[data-hours]') != null) {
          document.querySelector('[data-hours]').innerText = Math.floor((distance % (day)) / (hour));
        }
  
        if (document.querySelector('[data-minutes]') != null) {
          document.querySelector('[data-minutes]').innerText = Math.floor((distance % (hour)) / (minute));
        }
  
        if (document.querySelector('[data-seconds]') != null) {
          document.querySelector('[data-seconds]').innerText = Math.floor((distance % (minute)) / second);
        }
  
        // if (distance < 0) {
        //   clearInterval(x);
        // }
      }, second)
  }
  
  export default {
    init,
  }