// Automatically hide success messages after 5 seconds
document.addEventListener("DOMContentLoaded", function () {
  const successMessages = document.querySelectorAll(".flash.success");
  successMessages.forEach((message) => {
    setTimeout(() => {
      message.style.opacity = "0";
      setTimeout(() => {
        message.remove();
      }, 500); // Wait for the fade-out effect
    }, 5000); // Display for 5 seconds
  });

  // Add click-to-hide behavior for error messages
  const errorMessages = document.querySelectorAll(".flash.error");
  errorMessages.forEach((message) => {
    message.addEventListener("click", () => {
      message.style.opacity = "0";
      setTimeout(() => {
        message.remove();
      }, 500);
    });
  });
});
