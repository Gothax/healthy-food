<template>
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section about">
          <h2 class="logo-text">MyWebsite</h2>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce at venenatis urna, eget bibendum justo. Sed euismod lorem non magna auctor, sit amet consectetur neque consectetur.
          </p>
          <div class="contact">
            <span><i class="fas fa-phone"></i> &nbsp; 123-456-789</span>
            <span><i class="fas fa-envelope"></i> &nbsp; info@mywebsite.com</span>
          </div>
        </div>
  
        <div class="footer-section links">
          <h2>Quick Links</h2>
          <br>
          <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">Contact</a></li>
          </ul>
        </div>
  
        <div class="footer-section social">
          <h2>Follow Us</h2>
          <br>
          <div class="social-links">
            <a href="#"><i class="fab fa-facebook"></i></a>
            <a href="#"><i class="fab fa-twitter"></i></a>
            <a href="#"><i class="fab fa-instagram"></i></a>
            <a href="#"><i class="fab fa-linkedin"></i></a>
          </div>
        </div>
      </div>
  
      <div class="footer-bottom">
        &copy; 2024 MyWebsite | Designed by You
      </div>
    </footer>
  </template>
  
  <script>
  export default {
    name: 'Footer',
  };
  </script>
  
  <style scoped>
  .footer {
    background-color: #FFF6EE;
    color: black;
    padding: 30px 0;
    position: relative;
    bottom: 0;
    width: 100%;
  }
  
  .footer-content {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    max-width: 1200px;
    margin: auto;
    padding: 0 20px;
  }
  
  .footer-section {
    flex: 1;
    padding: 20px;
  }
  
  .footer-section h2 {
    margin-bottom: 15px;
  }
  
  .footer-section p {
    line-height: 1.6;
  }
  
  .footer-section .contact span,
  .footer-section .social-links a {
    display: block;
    margin: 10px 0;
  }
  
  .footer-section .social-links a {
    margin-right: 10px;
  }
  
  .footer-bottom {
    text-align: center;
    padding: 20px;
    background-color: #FFF6EE;
    margin-top: 20px;
  }
  
  .logo-text {
    font-size: 24px;
    font-weight: bold;
  }
  
  .footer-section ul {
    list-style: none;
    padding: 0;
  }
  
  .footer-section ul li {
    margin-bottom: 10px;
  }
  
  .footer-section ul li a {
    color: black;
    text-decoration: none;
  }
  
  .footer-section ul li a:hover {
    text-decoration: underline;
  }
  
  .social-links a {
    font-size: 20px;
    color: black;
  }
  
  .social-links a:hover {
    color: #d1d1d1;
  }
  </style>
  