#!/bin/bash

# test_poem_patches.sh
# Tests patching of two poems with multiple changes using embedded diff -u patches.

# Check for gpatch (GNU patch)
if ! command -v gpatch &> /dev/null; then
    echo "Error: gpatch (GNU patch) is not installed. Install it with 'brew install gpatch' on macOS."
    exit 1
fi

# Check for od (for debugging)
if ! command -v od &> /dev/null; then
    echo "Error: od command is not installed."
    exit 1
fi

# Logging setup
LOG_FILE="test_poem_patches.log"
echo "=== test_poem_patches.log ===" > "$LOG_FILE"
echo "Starting patch test process at $(date)" >> "$LOG_FILE"

# Clean up existing files to ensure a fresh start
rm -f SecondComing.txt HenryV-3-3.txt SecondComing_modified.txt HenryV-3-3_modified.txt second_coming_patch.diff henry_v_patch.diff SecondComing_to_patch.txt HenryV-3-3_to_patch.txt
echo "Cleaned up existing files to ensure a fresh start." | tee -a "$LOG_FILE"

# Create original poems
cat > SecondComing.txt << 'EOF'
Turning and turning in the widening gyre   
The weasel cannot hear the wrangler;
Things fall apart; the centre cannot hold;
Mere anarchy is loosed upon the world,
The blood-dimmed tide is loosed, and everywhere   
The ceremony of innocence is drowned;
The best lack all conviction, while the worst   
Are full of passionate intensity.

Surely some revelation is at hand;
Surely the Second Coming is at hand.   
The Second Coming! Hardly are those words out   
When a vast image out of Spiritus Mundi
Troubles my sight: somewhere in sands of the desert   
A shape with lion body and the head of a man,   
A gaze blank and pitiless as the sun,   
Is moving its slow thighs, while all about it   
Reel shadows of the indignant desert birds.   
The darkness drops again; but now I know   
That twenty centuries of stony sleep
Were vexed to nightmare by a rocking cradle,   
And what smooth beast, its hour come round at last,   
Slouches towards Bethlehem to be born?
EOF

cat > HenryV-3-3.txt << 'EOF'
How yet resolves the Governor of the town?
This is the latest parle we will admit.
Therefore to our best mercy give yourselves
Or, like to men proud of destruction,
Defy us to our worst. For, as I am a soldier,
A name that in my thoughts becomes me best,
If I begin the batt’ry once again,
I will not leave the half-achieved Harfleur
Till in her ashes she lie burièd.
The gates of mercy shall be all shut up,
And the fleshed soldier, rough and hard of heart,
In liberty of bloody hand, shall range
With conscience wide as hell, mowing like grass
Your fresh fair virgins and your flow’ring infants.
What is it then to me if impious war,
Arrayed in flames like to the prince of fiends,
Do with his smirched complexion all fell feats
Enlinked to waste and desolation?
What is ’t to me, when you yourselves are cause,
If your pure maidens fall into the hand
oF hOt AnD fOrCiNg ViOlAtIoN?
What rein can hold licentious wickedness
When down the hill he holds his fierce career?
We may as bootless spend our vain command

Upon th’ enragèd soldiers in their spoil
As send precepts to the Leviathan
To come ashore. Therefore, you men of Harfleur,
Take pity of your town and of your people
Whiles yet my soldiers are in my command,
Whiles yet the cool and temperate wind of grace
O’erblows the filthy and contagious clouds
Of heady murder, spoil, and villainy.
If not, why, in a moment look to see
The blind and bloody soldier with foul hand
Desire the locks of your shrill-shrieking daughters,
Your fathers taken by the silver beards
And their most reverend heads dashed to the walls,
Your naked infants spitted upon pikes
Whiles the mad mothers with their howls confused
Do break the clouds, as did the wives of Jewry
At Herod’s bloody-hunting slaughtermen.
What say you? Will you yield and this avoid
Or, guilty in defense, be thus destroyed?
EOF

echo "Created original poems: SecondComing.txt and HenryV-3-3.txt" | tee -a "$LOG_FILE"

# Create copies of the original files for patching
cp SecondComing.txt SecondComing_to_patch.txt
cp HenryV-3-3.txt HenryV-3-3_to_patch.txt
echo "Created copies for patching: SecondComing_to_patch.txt and HenryV-3-3_to_patch.txt" | tee -a "$LOG_FILE"

# Create expected modified versions for verification
cat > SecondComing_modified.txt << 'EOF'
Turning and turning in the widening gyre   
The falcon cannot hear the wrangler;
Things fall apart; the centre cannot hold;
Mere anarchy is loosed upon the world,
The blood-dimmed tide is loosed, and everywhere   
The ceremony of innocence is drowned;
The best lack all conviction, while the worst   
Are full of passionate intensity.

Surely some prophecy is at hand;
Surely the Second Coming is at hand.   
The Second Coming! Hardly are those words out   
When a vast image out of Spiritus Mundi
Troubles my sight: somewhere in sands of the desert   
A shape with lion body and the head of a man,   
A gaze blank and pitiless as the sun,   
Is moving its mighty thighs, while all about it   
Reel shadows of the indignant desert birds.   
The darkness drops again; but now I know   
That twenty centuries of stony sleep
Were vexed to nightmare by a rocking cradle,   
And what rough beast, its hour come round at last,   
Slouches towards Bethlehem to be born?
EOF

cat > HenryV-3-3_modified.txt << 'EOF'
How yet resolves the Mayor of the town?
This is the latest parle we will admit.
Therefore to our best mercy give yourselves
Or, like to men proud of destruction,
Defy us to our worst. For, as I am a soldier,
A name that in my thoughts becomes me best,
If I begin the batt’ry once again,
I will not leave the half-achieved Harfleur
Till in her ashes she lie burièd.
The gates of mercy shall be all shut up,
And the fleshed soldier, rough and hard of heart,
In liberty of bloody hand, shall range
With conscience wide as hell, mowing like grass
Your fresh fair virgins and your flow’ring infants.
What is it then to me if unholy war,
Arrayed in flames like to the prince of fiends,
Do with his smirched complexion all fell feats
Enlinked to waste and desolation?
What is ’t to me, when you yourselves are cause,
If your pure maidens fall into the hand
Of Hot And Forcing Violation?
What rein can hold licentious wickedness
When down the hill he holds his fierce career?
We may as bootless spend our vain command

Upon th’ enragèd soldiers in their spoil
As send precepts to the Leviathan
To come ashore. Therefore, you men of Harfleur,
Take pity of your town and of your people
Whiles yet my soldiers are in my command,
Whiles yet the cool and temperate wind of grace
O’erblows the filthy and contagious clouds
Of heady murder, spoil, and villainy.
If not, why, in a moment look to see
The blind and bloody soldier with foul hand
Desire the locks of your shrill-shrieking daughters,
Your fathers taken by the silver beards
And their most reverend heads dashed to the walls,
Your naked infants spitted upon pikes
Whiles the mad mothers with their howls confused
Do break the clouds, as did the wives of Jewry
At Herod’s bloody-hunting slaughtermen.
What say you? Will you yield and this avoid
Or, guilty in defense, be thus undone?
EOF

echo "Created expected modified poems for verification: SecondComing_modified.txt and HenryV-3-3_modified.txt" | tee -a "$LOG_FILE"

# Save the diff -u patches using printf to control newlines precisely
printf '%s\n' '--- SecondComing.txt	2025-04-21 23:14:00.000000000 -0700' \
'+++ SecondComing_modified.txt	2025-04-21 23:14:00.000000000 -0700' \
'@@ -1,4 +1,4 @@' \
' Turning and turning in the widening gyre   ' \
'-The weasel cannot hear the wrangler;' \
'+The falcon cannot hear the wrangler;' \
' Things fall apart; the centre cannot hold;' \
' Mere anarchy is loosed upon the world,' \
'' \
'@@ -7,5 +7,5 @@' \
' The best lack all conviction, while the worst   ' \
' Are full of passionate intensity.' \
'' \
'-Surely some revelation is at hand;' \
'+Surely some prophecy is at hand;' \
' Surely the Second Coming is at hand.   ' \
'' \
'@@ -14,10 +14,10 @@' \
' Troubles my sight: somewhere in sands of the desert   ' \
' A shape with lion body and the head of a man,   ' \
' A gaze blank and pitiless as the sun,   ' \
'-Is moving its slow thighs, while all about it   ' \
'+Is moving its mighty thighs, while all about it   ' \
' Reel shadows of the indignant desert birds.   ' \
' The darkness drops again; but now I know   ' \
' That twenty centuries of stony sleep' \
' Were vexed to nightmare by a rocking cradle,   ' \
'-And what smooth beast, its hour come round at last,   ' \
'+And what rough beast, its hour come round at last,   ' \
' Slouches towards Bethlehem to be born?' > second_coming_patch.diff

printf '%s\n' '--- HenryV-3-3.txt	2025-04-21 23:14:00.000000000 -0700' \
'+++ HenryV-3-3_modified.txt	2025-04-21 23:14:00.000000000 -0700' \
'@@ -1,24 +1,24 @@' \
'-How yet resolves the Governor of the town?' \
'+How yet resolves the Mayor of the town?' \
' This is the latest parle we will admit.' \
' Therefore to our best mercy give yourselves' \
' Or, like to men proud of destruction,' \
' Defy us to our worst. For, as I am a soldier,' \
' A name that in my thoughts becomes me best,' \
' If I begin the batt’ry once again,' \
' I will not leave the half-achieved Harfleur' \
' Till in her ashes she lie burièd.' \
' The gates of mercy shall be all shut up,' \
' And the fleshed soldier, rough and hard of heart,' \
' In liberty of bloody hand, shall range' \
' With conscience wide as hell, mowing like grass' \
' Your fresh fair virgins and your flow’ring infants.' \
'-What is it then to me if impious war,' \
'+What is it then to me if unholy war,' \
' Arrayed in flames like to the prince of fiends,' \
' Do with his smirched complexion all fell feats' \
' Enlinked to waste and desolation?' \
' What is ’t to me, when you yourselves are cause,' \
' If your pure maidens fall into the hand' \
'-oF hOt AnD fOrCiNg ViOlAtIoN?' \
'+Of Hot And Forcing Violation?' \
' What rein can hold licentious wickedness' \
' When down the hill he holds his fierce career?' \
' We may as bootless spend our vain command' \
'' \
'@@ -40,4 +40,4 @@' \
' Do break the clouds, as did the wives of Jewry' \
' At Herod’s bloody-hunting slaughtermen.' \
' What say you? Will you yield and this avoid' \
'-Or, guilty in defense, be thus destroyed?' \
'+Or, guilty in defense, be thus undone?' > henry_v_patch.diff

echo "Saved diff -u patches: second_coming_patch.diff and henry_v_patch.diff" | tee -a "$LOG_FILE"

# Debug: Inspect the patch files with od to check for unexpected characters
echo "Byte-level inspection of second_coming_patch.diff:" | tee -a "$LOG_FILE"
od -c second_coming_patch.diff | tee -a "$LOG_FILE"
echo "Byte-level inspection of henry_v_patch.diff:" | tee -a "$LOG_FILE"
od -c henry_v_patch.diff | tee -a "$LOG_FILE"

# Apply patches with -p0 and piped input
echo "Applying patch to SecondComing_to_patch.txt..." | tee -a "$LOG_FILE"
cat second_coming_patch.diff | gpatch -p0 --verbose SecondComing_to_patch.txt 2>&1 | tee -a "$LOG_FILE"
if [ ${PIPESTATUS[1]} -ne 0 ]; then
    echo "Error: Failed to apply patch to SecondComing_to_patch.txt" | tee -a "$LOG_FILE"
    exit 1
fi

echo "Applying patch to HenryV-3-3_to_patch.txt..." | tee -a "$LOG_FILE"
cat henry_v_patch.diff | gpatch -p0 --verbose HenryV-3-3_to_patch.txt 2>&1 | tee -a "$LOG_FILE"
if [ ${PIPESTATUS[1]} -ne 0 ]; then
    echo "Error: Failed to apply patch to HenryV-3-3_to_patch.txt" | tee -a "$LOG_FILE"
    exit 1
fi

# Verify results
echo "Verifying patched SecondComing_to_patch.txt..." | tee -a "$LOG_FILE"
diff SecondComing_to_patch.txt SecondComing_modified.txt >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    echo "Verification passed: SecondComing_to_patch.txt matches expected state." | tee -a "$LOG_FILE"
else
    echo "Error: Verification failed for SecondComing_to_patch.txt. Check $LOG_FILE for details." | tee -a "$LOG_FILE"
    exit 1
fi

echo "Verifying patched HenryV-3-3_to_patch.txt..." | tee -a "$LOG_FILE"
diff HenryV-3-3_to_patch.txt HenryV-3-3_modified.txt >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    echo "Verification passed: HenryV-3-3_to_patch.txt matches expected state." | tee -a "$LOG_FILE"
else
    echo "Error: Verification failed for HenryV-3-3_to_patch.txt. Check $LOG_FILE for details." | tee -a "$LOG_FILE"
    exit 1
fi

echo "All patches applied and verified successfully." | tee -a "$LOG_FILE"

# Clean up (optional, comment out if you want to inspect files)
# rm SecondComing.txt HenryV-3-3.txt SecondComing_modified.txt HenryV-3-3_modified.txt second_coming_patch.diff henry_v_patch.diff SecondComing_to_patch.txt HenryV-3-3_to_patch.txt