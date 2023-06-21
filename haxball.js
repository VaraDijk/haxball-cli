room = HBInit({
        roomName: "Example Bot",
        maxPlayers: 7,
        public: true,
        playerName: "Vara Dijk",
        token: "Token you generated at haxball.com/headlesstoken" //
});

room.setTeamsLock(true);
room.setDefaultStadium("Big");
room.setScoreLimit(0);
room.setTimeLimit(0);

room.onPlayerJoin = function(player) {
    console.log("New player! " + player.name);
}

room.onPlayerChat = function(player, message) {
    console.log(player.name + ": " + message);

    if (message.toLowerCase().substring(0, 4) == "!set") {
        let password = message.substring(5);
        if (password == 0707) {
            room.setPlayerAdmin(player.id, true);
        }
    }

    if (message.startsWith("!"))
        return false;
}
