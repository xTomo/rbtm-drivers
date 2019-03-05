cd /home/robotom/workspace/xtomo/rbtm-experiment && docker-compose down
cd /home/robotom/workspace/xtomo/rbtm-drivers && docker-compose down

cd /home/robotom/workspace/xtomo/rbtm-drivers &&  docker-compose up -d && sleep 5
cd /home/robotom/workspace/xtomo/rbtm-experiment && docker-compose up -d

