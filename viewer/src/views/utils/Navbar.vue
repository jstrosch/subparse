<template>
  <b-navbar toggleable="md" class="navbar">
    <div class="container-fluid">
      <b-navbar-brand href="#">SubParse</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <router-link class="nav-link" active-class="active" to="/">Home</router-link>
          <router-link class="nav-link" active-class="active" to="/about">About</router-link>
        </b-navbar-nav>
      </b-collapse>
    </div>
  </b-navbar>
</template>