This is a short script to parse a raw text dump (done with [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter)) of the 1v1-report channel from the CivFR discord and compute [TrueSkill](https://en.wikipedia.org/wiki/TrueSkill) ratings for each player. For 1v1 this is equivalent to ELO. This would converge to a representative rating faster in team and FFA games though.

* `leaderboard.txt` gives the rankings according to the order in which the match _were actually_ played.
* `leaderboard_N.txt` gives the rankings for 10 random shuffling of the matches orders, to show you the variability in such a ranking.
* If you look in the code, there is an example for how to use it for getting a probability of a balanced match:
```
CivFRMalm rating 22.9, Snippy rating 9.4, CivFRMalm vs. Snippy draw chance 0.23
Lege rating 23.1, CivFRMalm rating 22.9, Lege vs. CivFRMalm draw chance 0.72
```
* command used for the `DiscordChatExporter`: 
```
dotnet bin/Debug/net6.0/DiscordChatExporter.Cli.dll export -c 934946383566356582 -f PlainText
```

Quick hack provided under the:

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004
 
Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.
 
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.
