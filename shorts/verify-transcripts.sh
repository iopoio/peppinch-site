#!/bin/sh

set -eu

check() {
  page=$1
  first_sentence=$2
  if grep -Fq "$first_sentence" "$page"; then
    printf 'PASS %s\n' "$page"
  else
    printf 'FAIL %s: first transcript sentence missing\n' "$page" >&2
    exit 1
  fi
}

check shorts/chaebondi/metamorphosis.html '한 남자가 가족의 생계를 혼자 책임졌습니다.'
check shorts/chaebondi/overcoat.html '늘 무시받던 말단 직원이 있었습니다.'
check shorts/chaebondi/pride-and-prejudice.html '무례한 사람은 미워했고, 다정한 사람의 말은 의심하지 않았습니다.'
check shorts/chaebondi/the-picture-of-dorian-gray.html '진짜 위험한 말은, 내 가장 약한 두려움을 건드립니다.'
check shorts/chaebondi/king-lear.html '재산을 다 물려준 딸들에게, 아버지는 문밖으로 쫓겨났습니다.'
check shorts/naru/comparison.html '누군가의 좋은 소식을 본 뒤, 들고 있던 찻잔을 내려놓은 적이 있나요?'
check shorts/naru/control.html '계획을 다 세워둔 날일수록, 잠이 늦게 옵니다.'
check shorts/chaebondi/the-necklace.html '무도회 초대장을 받자, 아내는 울었습니다.'
check shorts/chaebondi/a-dolls-house.html '남편을 살리려, 아내는 몰래 돈을 빌렸습니다.'
check shorts/chaebondi/the-death-of-a-clerk.html '나흘 내내 사과했는데도, 돌아온 건 호통이었습니다.'
check shorts/chaebondi/the-death-of-ivan-ilyich.html '부고를 듣자, 친구들 얼굴엔 안도가 스쳤습니다.'
