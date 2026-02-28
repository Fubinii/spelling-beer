# spelling-bee
<center>
<img src="images/spelling-bee_crop.png" alt="spelling bee" width="150"/>
</center>

This is a python version of the Spelling Bee Game, adapting the setup by the New York Times puzzle. Currently, the game can be played by running the spelling-bee.py file.

---

You can use the provided dictionary 'en_US_60_SB.txt, which I tried to adjust so it replicates the word list of the NYT as closely as possible. It is based on the en_US.60 SCOWL word list, removing proper nouns, special characters and inappropriate language (the last one being a work-in-progress, feedback appreciated). I am also comparing it to the list of some of the NYT answers.
You can use your own dictionary as well.

---

To start the game you can either enter your own word or combination of letters, or you can use `!generate` to get set of 7 letters with at least two vowels. This option also guarantees that there is at least one pangram to be found!

---

To do:
- Implement ranking system as in NYT
- Graphical interface
- Clean up code


