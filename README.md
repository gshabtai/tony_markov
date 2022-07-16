# tony_markov
Open source markov chain to emulate tonychasebusiness. Created by Guy Shabtai.

# How it Works
This markov chain divides its operation into two components, called "pre" and "post". "pre" is some word (or words) that is used to predict the text following it, called "post". The program iterates over text, and makes a list of posts for every pre. Posts that are more prominent have a higher weight.

### Example 1: pre=1, post=1
For instance, if in our text is: *hello world i am guy shabtai and i created the tony markov program i am probably the greatest tony fan ever*

the word "i" is followed by "am" twice, and by "created" once, the mapping of the "pre" red would look like this

- i -> am 2 created 1

though the word "red" is not the only one being mapped. The full mapping would be:

- hello -> world 1
- world -> i 1
- i -> am 2 created 1
- am -> guy 1 probably 1
- guy -> shabtai 1
- shabtai -> and 1
- and -> i 1
- created -> the 1
- the -> tony 1 greatest 1
- tony -> markov 1 fan 1
- markov -> program 1
- program -> i 1
- probably -> the 1
- greatest -> tony 1
- fan -> ever 1

## Example 2: pre=1, post=2:

- hello -> world i 1
- world -> i am 1
- i -> am guy 1 created the 1 am probably 1
- am -> guy shabtai 1 probably the 1
- guy -> shabtai and 1
- shabtai -> and i 1
- and -> i created 1
- created -> the tony 1
- the -> tony markov 1 greatest tony 1
- tony -> markov program 1 fan ever 1
- markov -> program i 1
- program -> i am 1
- probably -> the greatest 1
- greatest -> tony fan 1

## Example 3: pre=1, post=2:

hello world -> i am 1
world i -> am guy 1
i am -> guy shabtai 1 probably the 1
am guy -> shabtai and 1
guy shabtai -> and i 1
shabtai and -> i created 1
and i -> created the 1
i created -> the tony 1
created the -> tony markov 1
the tony -> markov program 1
tony markov -> program i 1
markov program -> i am 1
program i -> am probably 1
am probably -> the greatest 1
probably the -> greatest tony 1
the greatest -> tony fan 1
greatest tony -> fan ever 1

# Implications
Increasing the size of pre increases how context-aware the AI is, as it is able to use more words to make its predictions. Increasing the size of post increases how close the prediction is to the original text.

Multiplicity is the metric used to determine how original the new text is. It is equal to the average number of options for each pre. In general, it's recommended for multiplciity to be 2, such there is an average of 2 choices per pre. 1 choice per pre would result in the output text being the same as the input text.
