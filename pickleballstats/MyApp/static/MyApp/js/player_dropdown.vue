<template>
    <div class="search-container">
    
      <div>
      <input type="text" placeholder="Search for Player" v-model="searchQuery" />
      <ul v-if="filteredPlayers.length > 0">
        <li v-for="player in filteredPlayers" :key="player.id" @click="selectPlayer(player)">
          {{ player.name }}
        </li>
      </ul> 
      </div>
  
      <div v-if="selectedPlayer" class="selected-player-stats">
        <h2>{{ selectedPlayerStats.name }}</h2>
        <p>Total Serves: {{ selectedPlayerStats.totalServes }}</p>
        <p>Serve Winners: {{ selectedPlayerStats.serveWins }}</p>
        <p>Serve Win Percentage: {{ serveWinPercentage }}%</p> 
      </div>
    </div>
  </template>

<script>
export default {
  data() {
    return {
      players: [
        { id: 1, name: 'Anna Leigh Waters', totalServes: 200, serveWins: 16 }, 
        { id: 2, name: 'Ben Johns', totalServes: 254, serveWins: 35 },
        { id: 3, name: 'Etta Wright', totalServes: 134, serveWins: 6 },
        { id: 4, name: 'Tyson McGuffin', totalServes: 209, serveWins: 25 },
        { id: 5, name: 'Meghan Dizon', totalServes: 165, serveWins: 11 },
        { id: 6, name: 'Anna Bright', totalServes: 197, serveWins: 4 },
        { id: 7, name: 'James Ignatowich', totalServes: 215, serveWins: 10 },
        { id: 8, name: 'Leigh Waters', totalServes: 200, serveWins: 16 }, 
        { id: 9, name: 'Christian Alshon', totalServes: 254, serveWins: 35 },
        { id: 10, name: 'Dekel Bar', totalServes: 134, serveWins: 6 },
        { id: 11, name: 'Adam Stone', totalServes: 209, serveWins: 25 },
        { id: 12, name: 'Catherine Parenteau', totalServes: 165, serveWins: 11 },
        { id: 13, name: 'Hayden Patriquin', totalServes: 197, serveWins: 4 },
        { id: 14, name: 'Jaume Martinez-Vich', totalServes: 215, serveWins: 10 },
        // ... More players...
      ],
      selectedPlayer: null,
      searchQuery: ''
    };
  },
  computed: {
    filteredPlayers() {
      let results = []
      if (this.searchQuery === '') {
        return results  
      }
      else {
        results = this.players.filter(player => 
           player.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }

      return results.slice(0, 10); // Show only top 10
    },
    selectedPlayerStats() {
      // Avoid errors from attempting to display if no player is selected yet
      if (!this.selectedPlayer) return {}; 

      return this.players.find(player => player.id === this.selectedPlayer);
    },
    serveWinPercentage() {
      if (!this.selectedPlayerStats.totalServes) { return 0; } // Avoid division by zero

      return (this.selectedPlayerStats.serveWins / this.selectedPlayerStats.totalServes * 100).toFixed(1);
    }
  },
  methods: {
    selectPlayer(player) {
      this.selectedPlayer = player.id; 
      this.searchQuery = ''; // Optional  - Clears search 
    }
  }
}
</script>

<style>
/* Search Input Area */
.search-container input {
  padding: 8px 12px;
  border: 1px solid #ccc; 
  border-radius: 4px;  
  font-size: 18px;
  width: 300px; /* Adjust as needed */
}

/* Dropdown Results */
.search-container ul {
  list-style-type: none;
  margin: 0; 
  padding: 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  max-height: 200px; /* Limits dropdown height */
  overflow-y: auto; /* Enables scrolling if many results */
  position: absolute; /* For easy placement below the input */
}

.search-container li {
  padding: 8px 12px;
  cursor: pointer;
  background-color: #ffff;
}

.search-container li:hover {
  background-color: #f0f0f0; /* Highlight on hover */
}


/* Stats Display Area */
.selected-player-stats { /* Assuming you might add a container div later */
  margin-top: 10px;
  border: 1px solid #ddd;  /* Subtle border */
  padding: 10px;
  border-radius: 5px; /*  Rounded corners */
  width: 304px;
}

.selected-player-stats h2 {
  margin-bottom: 10px; /* Space between name and stats */
}

.selected-player-stats p {
  margin-bottom: 5px; 
}


</style>
