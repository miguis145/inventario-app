param(
    [Parameter(Mandatory = $true)]
    [ValidateSet(
        "tools",
        "tests",
        "docker-build",
        "docker-run",
        "trivy",
        "minikube",
        "rolling",
        "pod-recreate",
        "blue-green",
        "green",
        "blue",
        "readiness",
        "persistence",
        "dora"
    )]
    [string]$EvidenceId
)

$ErrorActionPreference = "Continue"
$projectRoot = Split-Path -Parent $PSScriptRoot
$evidenceDirectory = Join-Path $projectRoot "evidencias"
$terminalLines = [System.Collections.Generic.List[object]]::new()

function Add-TerminalCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Command,

        [Parameter(Mandatory = $true)]
        [scriptblock]$Action
    )

    $terminalLines.Add([pscustomobject]@{
        Kind = "command"
        Text = "PS C:\inventario-app> $Command"
    })

    $commandOutput = & $Action 2>&1 | Out-String
    $cleanOutput = $commandOutput.TrimEnd() -replace "`e\[[0-?]*[ -/]*[@-~]", ""

    if ([string]::IsNullOrWhiteSpace($cleanOutput)) {
        $cleanOutput = "(comando completado sin salida)"
    } else {
        $outputLines = @($cleanOutput -split "`r?`n")

        if ($outputLines.Count -gt 120) {
            $omittedCount = $outputLines.Count - 100
            $cleanOutput = @(
                $outputLines[0..39]
                "... $omittedCount lineas intermedias omitidas en la captura ..."
                $outputLines[($outputLines.Count - 60)..($outputLines.Count - 1)]
            ) -join "`r`n"
        }
    }

    $terminalLines.Add([pscustomobject]@{
        Kind = "output"
        Text = $cleanOutput
    })

    $terminalLines.Add([pscustomobject]@{
        Kind = "blank"
        Text = ""
    })
}

function Invoke-CmdOutput {
    param(
        [Parameter(Mandatory = $true)]
        [string]$CommandLine
    )

    & cmd.exe /d /c "$CommandLine 2>&1"
}

function Save-TerminalImage {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Title,

        [Parameter(Mandatory = $true)]
        [string]$FileName
    )

    Add-Type -AssemblyName System.Drawing

    $imageWidth = 1600
    $horizontalPadding = 54
    $contentWidth = $imageWidth - ($horizontalPadding * 2)
    $titleBarHeight = 76
    $metaHeight = 62

    $fontTitle = [System.Drawing.Font]::new("Segoe UI", 22, [System.Drawing.FontStyle]::Bold)
    $fontMeta = [System.Drawing.Font]::new("Segoe UI", 13, [System.Drawing.FontStyle]::Regular)
    $fontTerminal = [System.Drawing.Font]::new("Consolas", 18, [System.Drawing.FontStyle]::Regular)

    $measureBitmap = [System.Drawing.Bitmap]::new(1, 1)
    $measureGraphics = [System.Drawing.Graphics]::FromImage($measureBitmap)
    $measureGraphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

    $lineLayouts = [System.Collections.Generic.List[object]]::new()
    $contentHeight = 30

    foreach ($line in $terminalLines) {
        if ($line.Kind -eq "blank") {
            $lineHeight = 18
        } else {
            $measured = $measureGraphics.MeasureString(
                $line.Text,
                $fontTerminal,
                [System.Drawing.SizeF]::new($contentWidth, 20000)
            )
            $lineHeight = [Math]::Ceiling($measured.Height) + 10
        }

        $lineLayouts.Add([pscustomobject]@{
            Kind   = $line.Kind
            Text   = $line.Text
            Height = $lineHeight
        })
        $contentHeight += $lineHeight
    }

    $measureGraphics.Dispose()
    $measureBitmap.Dispose()

    $imageHeight = $titleBarHeight + $metaHeight + $contentHeight + 42
    $bitmap = [System.Drawing.Bitmap]::new($imageWidth, $imageHeight)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit

    $backgroundBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(11, 16, 32))
    $terminalBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(17, 24, 39))
    $barBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(31, 41, 55))
    $titleBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(238, 242, 255))
    $metaBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(147, 164, 190))
    $commandBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(169, 220, 118))
    $outputBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(229, 231, 235))
    $borderPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(52, 65, 91), 2)

    $graphics.FillRectangle($backgroundBrush, 0, 0, $imageWidth, $imageHeight)
    $graphics.FillRectangle($terminalBrush, 28, 28, $imageWidth - 56, $imageHeight - 56)
    $graphics.FillRectangle($barBrush, 28, 28, $imageWidth - 56, $titleBarHeight)
    $graphics.DrawRectangle($borderPen, 28, 28, $imageWidth - 57, $imageHeight - 57)

    $graphics.FillEllipse([System.Drawing.Brushes]::IndianRed, 54, 57, 18, 18)
    $graphics.FillEllipse([System.Drawing.Brushes]::Goldenrod, 84, 57, 18, 18)
    $graphics.FillEllipse([System.Drawing.Brushes]::MediumSeaGreen, 114, 57, 18, 18)
    $graphics.DrawString($Title, $fontTitle, $titleBrush, 160, 49)
    $graphics.DrawString(
        "Evidencia generada con una salida real del proyecto",
        $fontMeta,
        $metaBrush,
        54,
        122
    )

    $currentY = 28 + $titleBarHeight + $metaHeight

    foreach ($layout in $lineLayouts) {
        if ($layout.Kind -ne "blank") {
            $brush = if ($layout.Kind -eq "command") { $commandBrush } else { $outputBrush }
            $graphics.DrawString(
                $layout.Text,
                $fontTerminal,
                $brush,
                [System.Drawing.RectangleF]::new(
                    $horizontalPadding,
                    $currentY,
                    $contentWidth,
                    $layout.Height
                )
            )
        }

        $currentY += $layout.Height
    }

    $outputPath = Join-Path $evidenceDirectory $FileName
    $bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)

    $borderPen.Dispose()
    $backgroundBrush.Dispose()
    $terminalBrush.Dispose()
    $barBrush.Dispose()
    $titleBrush.Dispose()
    $metaBrush.Dispose()
    $commandBrush.Dispose()
    $outputBrush.Dispose()
    $fontTitle.Dispose()
    $fontMeta.Dispose()
    $fontTerminal.Dispose()
    $graphics.Dispose()
    $bitmap.Dispose()

    Write-Output $outputPath
}

Set-Location $projectRoot

switch ($EvidenceId) {
    "tools" {
        Add-TerminalCommand "node --version" { node --version }
        Add-TerminalCommand "npm.cmd --version" { npm.cmd --version }
        Add-TerminalCommand "git --version" { git --version }
        Add-TerminalCommand "docker --version" { docker --version }
        Add-TerminalCommand "kubectl version --client" { kubectl version --client }
        Add-TerminalCommand "minikube version" { minikube version }
        Save-TerminalImage "Evidencia 01 | Versiones instaladas" "01-versiones-herramientas.png"
    }

    "tests" {
        Add-TerminalCommand "npm.cmd test" { npm.cmd test }
        Save-TerminalImage "Evidencia 02 | Pruebas automaticas" "02-pruebas-automaticas.png"
    }

    "docker-build" {
        Add-TerminalCommand "docker build -t inventario-app:local ." {
            Invoke-CmdOutput "docker build -t inventario-app:local ."
        }
        Add-TerminalCommand "docker images inventario-app" {
            Invoke-CmdOutput "docker images inventario-app"
        }
        Save-TerminalImage "Evidencia 03 | Construccion multi-stage" "03-docker-build.png"
    }

    "docker-run" {
        Add-TerminalCommand "docker run -d --name inventario-local -p 3000:3000 inventario-app:local" {
            docker run -d --name inventario-local -p 3000:3000 inventario-app:local
        }
        Start-Sleep -Seconds 2
        Add-TerminalCommand "docker ps --filter name=inventario-local" {
            docker ps --filter name=inventario-local
        }
        Add-TerminalCommand "docker logs inventario-local" {
            docker logs inventario-local
        }
        Add-TerminalCommand "curl.exe http://localhost:3000/health" {
            Invoke-CmdOutput "curl.exe -sS http://localhost:3000/health"
        }
        Add-TerminalCommand "curl.exe http://localhost:3000/version" {
            Invoke-CmdOutput "curl.exe -sS http://localhost:3000/version"
        }
        Add-TerminalCommand "curl.exe http://localhost:3000/api/products" {
            Invoke-CmdOutput "curl.exe -sS http://localhost:3000/api/products"
        }
        Save-TerminalImage "Evidencia 04 | Contenedor local" "04-contenedor-local.png"
    }

    "trivy" {
        $trivyCommand = "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v trivy-cache:/root/.cache/ aquasec/trivy:0.72.0 image --quiet --timeout 10m --db-repository public.ecr.aws/aquasecurity/trivy-db:2 --scanners vuln --vuln-type os,library --format table --exit-code 1 --ignore-unfixed --severity CRITICAL inventario-app:local"
        Add-TerminalCommand $trivyCommand {
            Invoke-CmdOutput $trivyCommand
        }
        Save-TerminalImage "Evidencia 06 | Escaneo de seguridad con Trivy" "06-trivy.png"
    }

    "minikube" {
        Add-TerminalCommand "kubectl get nodes" { kubectl get nodes }
        Add-TerminalCommand "minikube -p ci-cd status" { minikube -p ci-cd status }
        Save-TerminalImage "Evidencia 08 | Minikube listo" "08-minikube-ready.png"
    }

    "rolling" {
        Add-TerminalCommand "kubectl apply -f k8s/deployment.yaml" {
            kubectl apply -f k8s/deployment.yaml
        }
        Add-TerminalCommand "kubectl apply -f k8s/service.yaml" {
            kubectl apply -f k8s/service.yaml
        }
        Add-TerminalCommand "kubectl rollout status deployment/inventario-app" {
            kubectl rollout status deployment/inventario-app --timeout=180s
        }
        Add-TerminalCommand "kubectl get deployments" {
            kubectl get deployments
        }
        Add-TerminalCommand "kubectl get pods -o wide" {
            kubectl get pods -o wide
        }
        Add-TerminalCommand "kubectl get service inventario-service" {
            kubectl get service inventario-service
        }
        Save-TerminalImage "Evidencia 09 | Rolling Update" "09-rolling-update.png"
    }

    "pod-recreate" {
        $podName = kubectl get pods -l app=inventario-app -o jsonpath="{.items[0].metadata.name}"
        Add-TerminalCommand "kubectl get pods -l app=inventario-app" {
            kubectl get pods -l app=inventario-app
        }
        Add-TerminalCommand "kubectl delete pod $podName" {
            kubectl delete pod $podName
        }
        Add-TerminalCommand "kubectl wait --for=condition=Ready pod -l app=inventario-app --timeout=180s" {
            kubectl wait --for=condition=Ready pod -l app=inventario-app --timeout=180s
        }
        Add-TerminalCommand "kubectl get pods -l app=inventario-app" {
            kubectl get pods -l app=inventario-app
        }
        Save-TerminalImage "Evidencia 10 | Recreacion de un pod" "10-recreacion-pod.png"
    }

    "blue-green" {
        Add-TerminalCommand "kubectl delete deployment inventario-app --ignore-not-found" {
            kubectl delete deployment inventario-app --ignore-not-found
        }
        Add-TerminalCommand "kubectl apply -f k8s/blue-green/deployment-blue.yaml" {
            kubectl apply -f k8s/blue-green/deployment-blue.yaml
        }
        Add-TerminalCommand "kubectl apply -f k8s/blue-green/deployment-green.yaml" {
            kubectl apply -f k8s/blue-green/deployment-green.yaml
        }
        Add-TerminalCommand "kubectl apply -f k8s/blue-green/service.yaml" {
            kubectl apply -f k8s/blue-green/service.yaml
        }
        Add-TerminalCommand "kubectl rollout status deployment/inventario-app-blue" {
            kubectl rollout status deployment/inventario-app-blue --timeout=180s
        }
        Add-TerminalCommand "kubectl rollout status deployment/inventario-app-green" {
            kubectl rollout status deployment/inventario-app-green --timeout=180s
        }
        Add-TerminalCommand "kubectl get pods --show-labels -l app=inventario-app" {
            kubectl get pods --show-labels -l app=inventario-app
        }
        Save-TerminalImage "Evidencia 11 | Blue y Green activos" "11-blue-green-activos.png"
    }

    "green" {
        Add-TerminalCommand "kubectl patch service inventario-service --type merge --patch-file patch-green.json" {
            kubectl patch service inventario-service --type merge --patch-file patch-green.json
        }
        Add-TerminalCommand 'kubectl get service inventario-service -o jsonpath="{.spec.selector.slot}"' {
            kubectl get service inventario-service -o jsonpath="{.spec.selector.slot}"
        }
        Add-TerminalCommand 'curl.exe "$URL/version"' {
            Invoke-CmdOutput "curl.exe -sS http://127.0.0.1:8080/version"
        }
        Save-TerminalImage "Evidencia 12 | Trafico dirigido a Green" "12-trafico-green.png"
    }

    "blue" {
        Add-TerminalCommand "kubectl patch service inventario-service --type merge --patch-file patch-blue.json" {
            kubectl patch service inventario-service --type merge --patch-file patch-blue.json
        }
        Add-TerminalCommand 'kubectl get service inventario-service -o jsonpath="{.spec.selector.slot}"' {
            kubectl get service inventario-service -o jsonpath="{.spec.selector.slot}"
        }
        Add-TerminalCommand 'curl.exe "$URL/version"' {
            Invoke-CmdOutput "curl.exe -sS http://127.0.0.1:8080/version"
        }
        Save-TerminalImage "Evidencia 13 | Rollback a Blue" "13-rollback-blue.png"
    }

    "readiness" {
        Add-TerminalCommand "kubectl rollout restart deployment/inventario-app-blue" {
            kubectl rollout restart deployment/inventario-app-blue
        }
        Start-Sleep -Seconds 2
        Add-TerminalCommand "kubectl get pods -l app=inventario-app,slot=blue" {
            kubectl get pods -l app=inventario-app,slot=blue
        }
        Add-TerminalCommand "kubectl rollout status deployment/inventario-app-blue" {
            kubectl rollout status deployment/inventario-app-blue --timeout=180s
        }
        Add-TerminalCommand "kubectl get pods -l app=inventario-app,slot=blue" {
            kubectl get pods -l app=inventario-app,slot=blue
        }
        Save-TerminalImage "Evidencia 14 | Readiness durante el reinicio" "14-readiness.png"
    }

    "persistence" {
        Add-TerminalCommand 'curl.exe -X POST "$URL/api/products" -H "Content-Type: application/json" --data-binary "@evidencias/product-request.json"' {
            Invoke-CmdOutput "curl.exe -sS -X POST http://127.0.0.1:8080/api/products -H Content-Type:application/json --data-binary @evidencias/product-request.json"
        }
        Add-TerminalCommand 'curl.exe "$URL/api/products"' {
            Invoke-CmdOutput "curl.exe -sS http://127.0.0.1:8080/api/products"
        }

        $selectedPod = (curl.exe -sS http://127.0.0.1:8080/version | ConvertFrom-Json).hostname
        Add-TerminalCommand "kubectl delete pod $selectedPod" {
            kubectl delete pod $selectedPod
        }
        Add-TerminalCommand "kubectl wait --for=condition=Ready pod -l app=inventario-app,slot=blue --timeout=180s" {
            kubectl wait --for=condition=Ready pod -l app=inventario-app,slot=blue --timeout=180s
        }

        $oldPortForwards = Get-CimInstance Win32_Process -Filter "Name = 'kubectl.exe'" |
            Where-Object { $_.CommandLine -like "*port-forward*inventario-service*8080:80*" }

        foreach ($oldPortForward in $oldPortForwards) {
            Stop-Process -Id $oldPortForward.ProcessId -ErrorAction SilentlyContinue
        }

        $portForwardOutput = Join-Path ([IO.Path]::GetTempPath()) "inventario-persistence-port-forward.out.log"
        $portForwardError = Join-Path ([IO.Path]::GetTempPath()) "inventario-persistence-port-forward.err.log"
        Start-Process -FilePath "kubectl.exe" `
            -ArgumentList @("port-forward", "service/inventario-service", "8080:80") `
            -WindowStyle Hidden `
            -RedirectStandardOutput $portForwardOutput `
            -RedirectStandardError $portForwardError
        Start-Sleep -Seconds 2

        Add-TerminalCommand 'curl.exe "$URL/api/products"' {
            Invoke-CmdOutput "curl.exe -sS http://127.0.0.1:8080/api/products"
        }
        Save-TerminalImage "Evidencia 15 | Persistencia local" "15-persistencia-local.png"
    }

    "dora" {
        Add-TerminalCommand 'git log --pretty=format:"%h | %cI | %s" -10' {
            git log --pretty=format:"%h | %cI | %s" -10
        }
        Add-TerminalCommand 'Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"' {
            Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"
        }
        Add-TerminalCommand 'Import-Csv evidencias/dora-deployments.csv | Format-Table version,commit_at,deployed_at,lead_time,result' {
            Import-Csv (Join-Path $projectRoot "evidencias\dora-deployments.csv") |
                Format-Table version, commit_at, deployed_at, lead_time, result -AutoSize
        }
        Save-TerminalImage "Evidencia 16 | Datos para metricas DORA" "16-metricas-dora.png"
    }
}
