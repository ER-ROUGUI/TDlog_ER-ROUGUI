window.onload = function () {
        const urlParams = new URLSearchParams(window.location.search);
        const gameId = urlParams.get("game-id");
        const playerName = urlParams.get("player-name");
        document.getElementById("game-id").value = gameId;
        document.getElementById("player-name").value = playerName;
        }   

        async function getPlayer(gameId, playerName) {
            const resource_url = host + "/get-player?game_id=" + gameId + "&player_name=" +
            playerName;
            const response = await getData(resource_url);
            if (!response.ok) {
            return {player_name: playerName, battle_field: {vessels: []}};
            } else {
            return response.json();
            }
            }
            window.onload = function() {
                const addVesselForm = document.getElementById("add-vessel-form");
                if (addVesselForm != null) {
                  addVesselForm.addEventListener("submit", add_vessel);
                }
              };
              
    const loadButton = document.getElementById("load-button");
    loadButton.addEventListener("click", function () {
    getPlayer(gameId, playerName).then(function (player) {
    updateTable(player.battle_field.vessels);
    });
    });
    
    const playButton = document.getElementById("play-button");
  playButton.addEventListener("click", redirectToPlayGame);

//#---appler mainteennat cette fonction----//
function redirectToPlayGame() {
  
  const gameId = document.getElementById("game-id").value;
  const playerName = document.getElementById("player-name").value;

  const redirectUrl = "play_game.html?game-id=" + gameId + "&player-name=" + playerName;
  window.location.href = redirectUrl;
}

        
    function updateTable(vessels) {
    const table = document.getElementById("vessels-table");
    }
