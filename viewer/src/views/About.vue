<template>
  <section>
    <div class="container">
      <div class="row">
        <h1>SubParse</h1>
        <hr/>
        <br/>
        <p>
          Subparse, is a modular framework developed by Josh Strochein, Aaron Baker, and Odin Bernstein. The framework is designed to parse and index malware files and present the information found during the parsing in a searchable web-viewer. The framework is modular, making use of a core parsing engine, parsing modules, and a variety of enrichers that add additional information to the malware indices. The main input values for the framework are directories of malware files, which the core parsing engine or a user-specified parsing engine parses before adding additional information from any user-specified enrichment engine all before indexing the information parsed into an elasticsearch index. The information gathered can then be searched and viewed via a web-viewer, which also allows for filtering on any value gathered from any file. There is currently 3 parsing engine, the default parsing modules (ELFParser, OLEParser and PEParser), and 4 enrichment modules (ABUSEEnricher, CAPEEnricher, STRINGEnricher and YARAEnricher ).

        </p>

        <h2>Socials</h2>
        <hr/>

        <!-- Card 1 -->
        <div class="col-md-6">
          <div class="card profile-card-1">
            <img
              src="https://avatars.githubusercontent.com/u/1920756?v=4"
              alt="profile-image"
              class="profile"
            />
            <div class="card-content">
              <h2>Josh Stroschein<small>Security Researcher</small></h2>
              <div class="icon-block">
                <a href="https://twitter.com/jstrosch"> <i class="fa fa-twitter"></i></a>
                <a href="https://github.com/jstrosch"> <i class="fa fa-github"></i></a>
                <a href="https://www.linkedin.com/in/joshstroschein/"> <i class="fa fa-linkedin"></i></a>
                <a href="https://www.youtube.com/c/DrJoshStroschein/featured"> <i class="fa fa-youtube"></i></a>
              </div>
            </div>
          </div>
        </div>
        <!-- Card 1 End -->
        <!-- Card 2 -->
       <div class="col-md-6">
          <div class="card profile-card-1">
            <img
              src="https://avatars.githubusercontent.com/u/7686813?v=4"
              alt="profile-image"
              class="profile"
            />
            <div class="card-content">
              <h2>Aaron Baker<small>Security Researcher</small></h2>
              <div class="icon-block">
                <a href="https://twitter.com/baker_wyo"> <i class="fa fa-twitter"></i></a>
                <a href="https://github.com/abaker2010"> <i class="fa fa-github"></i></a>
                <a href="https://www.linkedin.com/in/aaron-baker-207051167/"> <i class="fa fa-linkedin"></i></a>
              </div>
            </div>
          </div>
        </div>
        <!-- Card 2 End -->
      </div>
    </div>

    <footer>  
      <p> ACKNOWLEDGEMENTS : This research and all the co-authors have been supported by NSA Grant H98230-20-1-0326.</p>
    </footer>

  </section>
</template>

<style scoped>
@import url("https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css");
@import url("https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700");
@import url("https://fonts.googleapis.com/css?family=Libre+Baskerville:400,700");
footer {
  display:flex;
  color:#F0F8FF;
  height:10vh;
  justify-content:center;
  align-items:flex-end;
  font-family:Open Sans;
}

footer p {
  font-size: small;
}

body {
  font-family: "Open Sans", sans-serif;
}
*:hover {
  -webkit-transition: all 1s ease;
  transition: all 1s ease;
}
section {
  float: left;
  width: 100%;
  padding: 30px 0;
}
hr {
  color: #c2bdbd;
}

h2 {
  margin-top: 5%;
  color: #ebebeb;
  text-align: center;
  width: 100%;
}

h1 {
  /* float: left; */
  width: 100%;
  color: #ebebeb;
  margin-bottom: 30px;
  /* font-size: 14px; */
  text-align: center;
}
h1 span {
  font-family: "Libre Baskerville", serif;
  display: block;
  font-size: 45px;
  text-transform: none;
  margin-bottom: 20px;
  margin-top: 30px;
  font-weight: 700;
}
h1 a {
  color: #131313;
  font-weight: bold;
}

/*Profile Card 1*/
.profile-card-1 {
  font-family: "Open Sans", Arial, sans-serif;
  position: relative;
  float: left;
  overflow: hidden;
  width: 100%;
  color: #ffffff;
  text-align: center;
  height: 368px;
  border: none;
}
.profile-card-1 .background {
  width: 100%;
  vertical-align: top;
  opacity: 0.9;
  -webkit-filter: blur(2px);
  filter: blur(2px);
  -webkit-transform: scale(1.8);
  transform: scale(2.8);
}
.profile-card-1 .card-content {
  width: 100%;
  padding: 15px 25px;
  position: absolute;
  left: 0;
  top: 50%;
}
.profile-card-1 .profile {
  border-radius: 50%;
  position: absolute;
  bottom: 50%;
  left: 50%;
  max-width: 100px;
  opacity: 1;
  box-shadow: 3px 3px 20px rgba(0, 0, 0, 0.5);
  border: 2px solid rgba(255, 255, 255, 1);
  -webkit-transform: translate(-50%, 0%);
  transform: translate(-50%, 0%);
}
.profile-card-1 h2 {
  margin: 0 0 5px;
  font-weight: 600;
  font-size: 25px;
}
.profile-card-1 h2 small {
  display: block;
  font-size: 15px;
  margin-top: 10px;
}
.profile-card-1 i {
  display: inline-block;
  font-size: 16px;
  color: #ffffff;
  text-align: center;
  border: 1px solid #fff;
  width: 30px;
  height: 30px;
  line-height: 30px;
  border-radius: 50%;
  margin: 0 5px;
}
.profile-card-1 .icon-block {
  float: left;
  width: 100%;
  margin-top: 15px;
}
.profile-card-1 .icon-block a {
  text-decoration: none;
}
.profile-card-1 i:hover {
  background-color: #fff;
  color: #2e3434;
  text-decoration: none;
}



/*Profile Card 3*/
.profile-card-3 {
  font-family: 'Open Sans', Arial, sans-serif;
  position: relative;
  float: left;
  overflow: hidden;
  width: 100%;
  text-align: center;
  height:368px;
  border:none;
}
.profile-card-3 .background-block {
    float: left;
    width: 100%;
    height: 200px;
    overflow: hidden;
}
.profile-card-3 .background-block .background {
  width:100%;
  vertical-align: top;
  opacity: 0.9;
  -webkit-filter: blur(0.5px);
  filter: blur(0.5px);
   -webkit-transform: scale(1.8);
  transform: scale(2.8);
}
.profile-card-3 .card-content {
  width: 100%;
  padding: 15px 25px;
  color:#232323;
  float:left;
  /* background:#17a2b8; */
  height:50%;
  border-radius:0 0 5px 5px;
  position: relative;
  z-index: 9999;
}
.profile-card-3 .card-content::before {
    content: '';
    /* background: #17a2b8; */
    width: 120%;
    height: 100%;
    left: 11px;
    bottom: 51px;
    position: absolute;
    z-index: -1;
    transform: rotate(-13deg);
}
.profile-card-3 .profile {
  border-radius: 50%;
  position: absolute;
  bottom: 50%;
  left: 50%;
  max-width: 100px;
  opacity: 1;
  box-shadow: 3px 3px 20px rgba(0, 0, 0, 0.5);
  border: 2px solid rgba(255, 255, 255, 1);
  -webkit-transform: translate(-50%, 0%);
  transform: translate(-50%, 0%);
  z-index:99999;
}
.profile-card-3 h2 {
  margin: 0 0 5px;
  font-weight: 600;
  font-size:25px;
}
.profile-card-3 h2 small {
  display: block;
  font-size: 15px;
  margin-top:10px;
}
.profile-card-3 i {
  display: inline-block;
    font-size: 16px;
    color: #232323;
    text-align: center;
    border: 1px solid #232323;
    width: 30px;
    height: 30px;
    line-height: 30px;
    border-radius: 50%;
    margin:0 5px;
}
.profile-card-3 .icon-block{
    float:left;
    width:100%;
    margin-top:15px;
}
.profile-card-3 .icon-block a{
    text-decoration:none;
}
.profile-card-3 i:hover {
  background-color:#232323;
  color:#fff;
  text-decoration:none;
}

p {
  color: #ebebeb;
}

</style>
