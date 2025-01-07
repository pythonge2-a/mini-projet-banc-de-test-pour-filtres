# Vérifier si le dossier courant est un dépôt Git
if (-not (Test-Path -Path ".git")) {
    Write-Error "Le script doit être exécuté depuis un dépôt Git."
    exit
}

# Obtenir le nombre total de commits
$totalCommits = git rev-list --all --count

# Vérifier qu'il y a des commits
if (-not $totalCommits) {
    Write-Error "Aucun commit trouvé dans ce dépôt."
    exit
}

# Obtenir la liste des auteurs et leurs nombres de commits
$authors = git shortlog -s -n --all | ForEach-Object {
    $parts = $_ -split "\t"
    [PSCustomObject]@{
        Commits = $parts[0] -as [int]
        Author  = $parts[1]
    }
}

# Calculer les pourcentages et afficher les résultats
Write-Host "Dépôt Git : $(Get-Location)"
Write-Host "Total commits : $totalCommits`n"

$authors | ForEach-Object {
    $percentage = ($_.Commits / $totalCommits) * 100
    Write-Host "$($_.Author): $($_.Commits) commits ($([math]::Round($percentage, 2))%)"
}

# Ajouter une pause pour empêcher la fermeture immédiate
Read-Host "Appuyez sur Entrée pour quitter"
