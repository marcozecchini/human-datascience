/* eslint-disable */
<template>
  <div class="ping">
    <img alt="Sapienza logo" src="../assets/logo.jpeg">
    <br>
    <br>
    <p>Upload your image for discover which ancient god you look like!</p>
    <p>(At least according to our <a href="https://web.uniroma1.it/polomuseale/en/node/5653">museum</a>)</p>
    <input type="file" @change="onFileSelected">
    <button id="button" @click="onUpload">Upload</button>
    <br>
    <br>
    <div class="image-preview" v-if="imageData.length > 0">
      <img class="preview" :src="imageData">
    </div>
    <p>{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      selectedFile: [],
      msg: '',
      imageData: '',
    };
  },
  methods: {
    onFileSelected(event) {
      [this.selectedFile] = event.target.files;
      this.createImage(event.target.files);
    },
    onUpload() {
      const path = 'https://human-ds.herokuapp.com/image';
      const fd = new FormData();
      fd.append('image', this.selectedFile, this.selectedFile.name);
      axios.post(path, fd)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          this.msg = 'Il servizio è temporaneamente non disponibile';
          console.log(error);
        });
    },
    createImage(files) {
      if (files && files[0]) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imageData = e.target.result;
        };
        reader.readAsDataURL(files[0]);
      }
    },
  },
};
</script>
