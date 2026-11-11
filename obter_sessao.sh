#!/usr/bin/env bash
# Traz para o teu repositório os ficheiros de partida de uma sessão.
# Uso:  bash obter_sessao.sh 2
# Ficheiros que já tens não são tocados, por isso podes correr o comando
# as vezes que quiseres sem perder trabalho.
set -e
if [ -z "$1" ]; then echo "Uso: bash obter_sessao.sh <número da sessão>"; exit 1; fi
N=$(printf "%02d" "$1")
URL=$(tr -d '[:space:]' < .modulo_url)
git remote get-url modulo >/dev/null 2>&1 || git remote add modulo "$URL"
git fetch -q modulo main
if ! git cat-file -e "modulo/main:sessoes/$N.txt" 2>/dev/null; then
  echo "A Sessão $N ainda não foi publicada. Tenta mais perto da hora da sessão."; exit 1
fi
echo "Sessão $N:"
for f in sessoes/$N.txt $(git show "modulo/main:sessoes/$N.txt"); do
  if [ -e "$f" ]; then
    echo "  já existe, não mexi: $f"
  else
    git checkout modulo/main -- "$f"
    echo "  novo: $f"
  fi
done
echo "Próximo passo: git add . && git commit -m \"Ficheiros de partida da Sessão $N\""
