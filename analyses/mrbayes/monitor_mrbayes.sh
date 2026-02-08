#!/bin/bash
# =============================================================================
# Monitor MrBayes run and auto-update results when complete
# Run: nohup bash monitor_mrbayes.sh &
# =============================================================================

MRBAYES_DIR="/Users/yeyoruiz/Documents/00-conocarpus_project/conocarpus-phylogeny/analyses/mrbayes"
REPO_DIR="/Users/yeyoruiz/Documents/00-conocarpus_project/conocarpus-phylogeny"
LOG_FILE="$MRBAYES_DIR/mrbayes_run.log"
MONITOR_LOG="$MRBAYES_DIR/monitor.log"

echo "[$(date)] Monitor started. Watching MrBayes..." > "$MONITOR_LOG"

while true; do
    # Check if MrBayes is still running
    if ! pgrep -f "mb mrbayes_commands" > /dev/null 2>&1; then
        echo "[$(date)] MrBayes process not found. Checking if it completed..." >> "$MONITOR_LOG"

        # Check if consensus tree was generated (sign of successful completion)
        if [ -f "$MRBAYES_DIR/combretaceae_mrbayes.con.tre" ]; then
            echo "[$(date)] SUCCESS: MrBayes completed! Consensus tree found." >> "$MONITOR_LOG"

            # Copy results to repo
            echo "[$(date)] Copying results to repository..." >> "$MONITOR_LOG"

            # Copy consensus tree to bayesian results
            cp "$MRBAYES_DIR/combretaceae_mrbayes.con.tre" "$REPO_DIR/results/trees/bayesian/"

            # Copy tree probabilities if exists
            if [ -f "$MRBAYES_DIR/combretaceae_mrbayes.trprobs" ]; then
                cp "$MRBAYES_DIR/combretaceae_mrbayes.trprobs" "$REPO_DIR/results/trees/bayesian/"
            fi

            # Copy partition table if exists
            if [ -f "$MRBAYES_DIR/combretaceae_mrbayes.parts" ]; then
                cp "$MRBAYES_DIR/combretaceae_mrbayes.parts" "$REPO_DIR/results/trees/bayesian/"
            fi

            # Copy parameter logs
            cp "$MRBAYES_DIR/combretaceae_mrbayes.run1.p" "$REPO_DIR/results/logs/" 2>/dev/null
            cp "$MRBAYES_DIR/combretaceae_mrbayes.run2.p" "$REPO_DIR/results/logs/" 2>/dev/null

            # Extract ASDSF from log
            FINAL_ASDSF=$(grep "Average standard deviation of split frequencies" "$LOG_FILE" | tail -1 | awk '{print $NF}')

            # Extract final generation
            FINAL_GEN=$(grep -E "^\s+[0-9]+" "$LOG_FILE" | tail -1 | awk '{print $1}')

            # Get consensus tree topology
            CON_TREE=""
            if [ -f "$MRBAYES_DIR/combretaceae_mrbayes.con.tre" ]; then
                CON_TREE=$(grep "tree con_50_majrule" "$MRBAYES_DIR/combretaceae_mrbayes.con.tre" | head -1)
            fi

            echo "[$(date)] Final ASDSF: $FINAL_ASDSF" >> "$MONITOR_LOG"
            echo "[$(date)] Final generation: $FINAL_GEN" >> "$MONITOR_LOG"
            echo "[$(date)] All results copied to repository." >> "$MONITOR_LOG"

            # Send notification
            osascript -e 'display notification "MrBayes analysis complete! Results copied to conocarpus-phylogeny repo." with title "MrBayes Done" sound name "Glass"' 2>/dev/null

            echo "[$(date)] Monitor complete. Exiting." >> "$MONITOR_LOG"
            exit 0

        else
            echo "[$(date)] WARNING: MrBayes stopped but no consensus tree found. Check mrbayes_run.log for errors." >> "$MONITOR_LOG"
            osascript -e 'display notification "MrBayes stopped without completing. Check logs." with title "MrBayes Error" sound name "Basso"' 2>/dev/null
            exit 1
        fi
    fi

    # Log progress every check
    CURRENT_ASDSF=$(grep "Average standard deviation of split frequencies" "$LOG_FILE" | tail -1 | awk '{print $NF}')
    CURRENT_GEN=$(grep -E "^\s+[0-9]+" "$LOG_FILE" | tail -1 | awk '{print $1}')
    echo "[$(date)] Running... Gen: $CURRENT_GEN/5000000 | ASDSF: $CURRENT_ASDSF" >> "$MONITOR_LOG"

    # Check every 60 seconds
    sleep 60
done
