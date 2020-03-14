$dateStart = $request->get('date_start');
            $dateEnd = $request->get('date_end');            $listUser = SurveyAction::select('user_id')
                ->where('survey_id', $request->get('survey'));
                if(!empty($dateStart)){
                    $listUser =  $listUser->where('started_at', '>=', $dateStart);
                }
                if(!empty($dateEnd)){
                    $listUser =  $listUser->where('completed_at', '<=', $dateEnd);
                }
            $listUser = $listUser->distinct()->get();            $repeat = [];
            $repeat['new'] = 0;
            $repeat['repeat'] = 0;
            foreach($listUser as $ls) {
                $checkData = UseBrand::where('user_id', $ls->user_id)
                    ->where('brand_id', $request->get('brand'));
                    if (!empty($dateStart)) {
                        $checkData = $checkData->where('created_at', '>=', $dateStart);
                    }
                    if (!empty($dateEnd)) {
                        $checkData = $checkData->where('created_at', '<=', $dateEnd);
                    }
                    $checkData = $checkData->first();
                if(!$checkData) {
                    $repeat['new'] += 1;
                } else {
                    $repeat['repeat'] += 1;
                }
            }            if(!empty($dateStart)) {
                $whereDateStart = ' and date_format(survey_answers.created_at, "%Y-%m-%d") >= "'.$dateStart.'"';
            } else {
                $whereDateStart = '';
            }            if(!empty($dateEnd)) {
                $whereDateEnd = ' and date_format(survey_answers.created_at, "%Y-%m-%d") <= "'.$dateEnd.'"';
            } else {
                $whereDateEnd = '';
            }            $data = \DB::select(\DB::raw('
                select survey_questions.question_text , survey_questions.type,
                concat( if(int_answer is null, "", survey_options.option_text),if(datetime_answer is null, "", datetime_answer),if(time_answer is null, "", time_answer) ) as full_answer,
                count(survey_answers.id) as answer
                from survey_answers join survey_questions on survey_questions.id = survey_answers.question_id and survey_questions.type NOT IN ("text", "date", "time")
                left join survey_options on survey_answers.int_answer = survey_options.id
                where survey_questions.survey_id = '.$request->get("survey").$whereDateStart.$whereDateEnd.'
                and survey_questions.deleted_at is null
                group by survey_questions.id,survey_options.id
            '));