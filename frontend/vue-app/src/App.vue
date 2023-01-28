<template>
  <header><h1>GitHub Repository Explorer</h1></header>

  <section id="repositories">
    <div>
      <p>
        Please enter the username of the person whose repositories you want to
        list.
      </p>
      <input
        type="text"
        v-model="inputData"
        v-on:keyup.enter="loadData(inputData)"
      />
      <button v-if="isLoading">Loading...</button>
      <button v-else @click="loadData(inputData)">Fetch</button>
      <div v-if="errorMessage" class="alert" @click="resetErrorMessage()">
        <span class="closebtn">&times; </span>
        {{ errorMessage }}
      </div>
    </div>
    <h1 v-if="(repositories.length > 0) && (username.length > 0)">Repositories of {{ username }}</h1>
    <ul>
      <li
        v-for="repository in repositories"
        :key="repository.name"
        class="high-level"
      >
        <h2>
          <a :href="repository.url" target="_blank">{{ repository.name }}</a>
        </h2>
        <ul>
          <li><b>Description:</b> {{ repository.description }}</li>
          <li><b>Stars:</b> {{ repository.stars }}</li>
          <li><b>Commits:</b> {{ repository.commits }}</li>
        </ul>
      </li>
    </ul>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      errorMessage: "",
      inputData: "",
      isLoading: false,
      loadError: null,
      repositories: [],
      username: "",
      url: "http://127.0.0.1:8000/",
    };
  },
  methods: {
    loadData(username) {
      if (!this.isLoading) {
        this.isLoading = true;
        this.errorMessage = "";
        axios
          .get(this.url + username + "/")
          .then((response) => {
            const results = [];
            for (const id in response.data) {
              results.push({
                url: response.data[id]["url"],
                name: response.data[id]["name"],
                description: response.data[id]["description"],
                stars: response.data[id]["stars"],
                commits: response.data[id]["commits"],
              });
            }
            this.repositories = results;
            this.username = username;
          })
          .catch((error) => {
            this.repositories = [];
            if (error.response.data.detail["message"]) {
              this.errorMessage = error.response.data.detail["message"];
            }
          })
          .finally(() => {
            this.isLoading = false;
          });
      }
    },
    resetErrorMessage() {
      this.errorMessage = "";
    },
  },
};
</script>


<style>
@import url("https://fonts.googleapis.com/css2?family=Jost&display=swap");

* {
  box-sizing: border-box;
}

html {
  font-family: "Jost", sans-serif;
}

header {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  margin: 3rem auto;
  border-radius: 10px;
  padding: 1rem;
  background-color: #58004d;
  color: white;
  text-align: center;
  width: 90%;
  max-width: 50rem;
}

div {
  margin: 1rem auto;
}

input {
  margin: 1rem;
}

#repositories {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  margin: 3rem auto;
  border-radius: 10px;
  padding: 1rem;
  text-align: center;
  width: 90%;
  max-width: 50rem;
}

#app ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

#app h2 {
  font-size: 2rem;
  border-bottom: 4px solid #ccc;
  color: #58004d;
  margin: 0 0 1rem 0;
}

#app a {
  text-decoration: none;
  color: inherit;
}

#repositories h1 {
  font-size: 1.25rem;
  font-weight: bold;
  border: 1px solid #393338;
  background-color: #393338;
  color: white;
  padding: 0.5rem;
  border-radius: 20px;
  margin: 2rem auto 3rem auto;
  width: 90%;
  max-width: 50rem;
}

#repositories p {
  font-size: 1.25rem;
  font-weight: bold;
  max-width: 50rem;
}

#app button {
  font: inherit;
  cursor: pointer;
  border-radius: 25px;
  border: 1px solid #393338;
  background-color: #4f4b4f;
  color: white;
  padding: 0.05rem 1rem;
  box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.26);
}

#app button:hover,
#app button:active {
  border: 1px solid #58004d;
  background-color: #72007a;
  box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.26);
}

#app li.high-level {
  margin: 1rem auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
}

#app li {
  margin: 0.4rem auto;
  padding: 0.4rem;
  width: 90%;
  max-width: 50rem;
}

.alert {
  font: inherit;
  cursor: pointer;
  border-radius: 25px;
  border: 1px solid #c62828;
  background-color: #c62828;
  color: white;
  margin: 2rem auto;
  padding: 0.05rem 1rem;
  box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.26);
  width: fit-content;
}

.closebtn {
  margin-left: 0.5rem;
  color: white;
  font-weight: bold;
  float: right;
  font-size: 22px;
  line-height: 20px;
  transition: 0.3s;
}

.closebtn:hover {
  color: black;
}
</style>
