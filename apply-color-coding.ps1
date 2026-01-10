$file = 'x:\dev\devnull\docs\FCOM_AgielColorCodedLoadOrder.html'
$lines = Get-Content $file

$inTableBody = $false
$output = @()
$currentEntry = @()

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    
    if ($line -match '<tbody>') {
        $inTableBody = $true
    }
    elseif ($line -match '</tbody>') {
        $inTableBody = $false
    }
    
    # Check if this is a row start
    if ($inTableBody -and $line -match '^                    <tr>$') {
        # Collect the entire entry
        $currentEntry = @($line)
        $j = $i + 1
        
        # Read until we find the closing </tr>
        while ($j -lt $lines.Count -and $lines[$j] -notmatch '</tr>') {
            $currentEntry += $lines[$j]
            $j++
        }
        if ($j -lt $lines.Count) {
            $currentEntry += $lines[$j] # Add closing </tr>
        }
        
        # Join to analyze
        $entryText = $currentEntry -join "`n"
        
        # Determine color class
        $colorClass = ""
        
        # Check category
        if ($entryText -match '<td class="category">Gameplay</td>') {
            $colorClass = "row-gameplay"
        }
        elseif ($entryText -match '<td class="category">Spells</td>') {
            $colorClass = "row-gameplay"
        }
        elseif ($entryText -match '<td class="category">NPC</td>') {
            $colorClass = "row-gameplay"
        }
        elseif ($entryText -match '<td class="category">Textures</td>') {
            $colorClass = "row-aesthetic"
        }
        elseif ($entryText -match '<td class="category">Scenery</td>') {
            $colorClass = "row-aesthetic"
        }
        elseif ($entryText -match '<td class="category">Water</td>') {
            $colorClass = "row-aesthetic"
        }
        elseif ($entryText -match '<td class="category">Lights</td>') {
            $colorClass = "row-aesthetic"
        }
        elseif ($entryText -match '<td class="category">Mesh replacement</td>') {
            $colorClass = "row-aesthetic"
        }
        elseif ($entryText -match '<td class="category">Sounds</td>') {
            $colorClass = "row-aesthetic"
        }
        elseif ($entryText -match '<td class="category">Official Plugin</td>') {
            $colorClass = "row-official"
        }
        elseif ($entryText -match '<td class="category">Official plugin</td>') {
            $colorClass = "row-official"
        }
        elseif ($entryText -match '<td class="category">Patch</td>') {
            $colorClass = "row-patch"
        }
        elseif ($entryText -match '<td class="category">Quest</td>') {
            $colorClass = "row-new-content"
        }
        elseif ($entryText -match '<td class="category">House</td>') {
            $colorClass = "row-new-content"
        }
        elseif ($entryText -match '<td class="category">Armor Weapons</td>') {
            $colorClass = "row-new-content"
        }
        elseif ($entryText -match '<td class="category">Performance</td>') {
            $colorClass = "row-patch"
        }
        elseif ($entryText -match '<td class="category">Player Character</td>') {
            $colorClass = "row-aesthetic"
        }
        elseif ($entryText -match '<td class="category"></td>' -or $entryText -match '<td class="category">Core</td>') {
            # Empty category or Core - determine by mod name/group
            if ($entryText -match 'Unique Landscapes' -or $entryText -match 'Better Cities' -or $entryText -match 'Fellan Cities') {
                $colorClass = "row-aesthetic"
            }
            elseif ($entryText -match 'Supreme Magicka' -or $entryText -match 'MMM') {
                $colorClass = "row-gameplay"
            }
            else {
                $colorClass = "row-gameplay"  # Default for empty
            }
        }
        
        # Check for conflicts - add severe class
        if ($entryText -match 'Customized' -or $entryText -match 'Serious conflicts' -or $entryText -match 'Several .* conflicts') {
            if ($colorClass) {
                $colorClass += " row-conflict-severe"
            } else {
                $colorClass = "row-conflict-severe"
            }
        }
        
        # Apply color class
        if ($colorClass) {
            $currentEntry[0] = "                    <tr class=`"$colorClass`">"
        }
        
        # Add to output
        $output += $currentEntry
        
        # Skip ahead
        $i = $j
    }
    else {
        $output += $line
    }
}

# Write output
$output | Set-Content $file

Write-Host "Color coding complete!"
