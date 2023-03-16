query02 = "SELECT TOP({0}) * FROM dbo.a3_mockQuiz WHERE D BETWEEN {1} AND {2};".format(valueN, startRange, endRange)

        for perQuery in range(5):
            timeBeforeQuery = time()
            if lenOutputQ02 == 0:
                cursor02.execute(query02)
                outputQ02 = cursor02.fetchall()
                lenOutputQ02 = len(outputQ02)
                redis_client.set("lenOutputQ02",(lenOutputQ02))
            elif lenOutputQ02 != 0:
                print(lenOutputQ02)
                
            timeAfterQuery = time()
            temp = timeAfterQuery - timeBeforeQuery
            timeOfExecution.append(temp)
            print("--", timeOfExecution)
                
        connectDB_02.close()
        redisGet = redis_client.get("lenOutputQ4")
        lenOutputQ02 = int(redisGet)
        totalTimeOfExecution = sum(timeOfExecution)
        
        # print("--outputQ1--", outputQ1)
        recordCount = len(outputQ02)
        if len(outputQ02) < 1:
            return render_template('q02_withRedisEachQuery.html', onFailure = "Records not found")
        else:
            return render_template('q02_withRedisEachQuery.html', onSuccess = recordCount , outputQ02 = outputQ02, timeOfExecution = timeOfExecution, totalTimeOfExecution = totalTimeOfExecution, countFromRedis = lenOutputQ02 )
