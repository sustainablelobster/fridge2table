$ErrorActionPreference = "Stop"

function Test-Newer($file1, $file2) {
    try {
        $file1Details = Get-Item -Path $file1
        $file2Details = Get-Item -Path $file2
        return $file1Details.LastWriteTime -gt $file2Details.LastWriteTime
    } catch {
        return $true
    }
}

function Initialize-PythonVenv {
    $venv = ".cmsc495_venv"
    $requirementsStamp = "$venv\.requirements.stamp"

    if (-not (Test-Path -Path $venv)) {
        Write-Host -Object "Creating Python virtual environment..."
        python -m venv $venv
    }

    . "$venv\Scripts\Activate.ps1"

    python -c "import pre_commit" 2>&1 | Out-Null
    if (-not $?) {
        Write-Host -Object "Installing pre-commit package..."
        pip install pre-commit
    }

    if (Test-Newer "requirements.txt" $requirementsStamp) {
        Write-Host -Object "Installing Python requirements..."
        pip install -r requirements.txt
        Out-File -FilePath $requirementsStamp -InputObject $null
    }
}

function Install-PreCommitHooks {
    $precommitStamp = ".git\.pre-commit.stamp"

    if (Test-Newer ".pre-commit-config.yaml" $precommitStamp) {
        Write-Host -Object "Installing pre-commit hooks..."
        pre-commit install
        Out-File -FilePath $precommitStamp -InputObject $null
    }
}

Initialize-PythonVenv && Install-PreCommitHooks
