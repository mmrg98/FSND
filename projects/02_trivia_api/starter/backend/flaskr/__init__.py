import os
from flask import flash, Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
	page = request.args.get('page', 1, type=int)
	start = (page - 1) * QUESTIONS_PER_PAGE
	end = start + QUESTIONS_PER_PAGE

	questions = [question.format() for question in selection]
	current_questions = questions[start:end]

	return current_questions

def create_app(test_config=None):

	app = Flask(__name__, instance_relative_config=True)


	setup_db(app)

	CORS(app)


	cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

	# CORS Headers
	@app.after_request
	def after_request(response):
		response.headers.add(
			'Access-Control-Allow-Headers',
			'Content-Type, Authorization,true')

		response.headers.add(
			'Access-Control-Allow-Methods',
			'GET,POST,DELETE,OPTIONS')

		return response


	@app.route('/questions', methods=['GET'])
	def get_questions():
		'''return all questions and each page contains 10 questions only  '''
		selection= Question.query.order_by(Question.id).all()
		current_questions = paginate_questions(request, selection)
		categories = Category.query.order_by(Category.id).all()
		categories = {category.id: category.type for category in categories}

		if len(current_questions) == 0:
			abort(404)

		return jsonify({
			'success':True,
			'questions': current_questions,
			'total_questions': len(Question.query.all()),
			'current_category':"category",
			'categories': categories
		})


	@app.route('/questions/<int:question_id>', methods=['DELETE'])
	def delete_question(question_id):
		'''take  question_id as parameter and
		 delete the question with this id '''

		try:
			question = Question.query.filter(
			Question.id == question_id
			).one_or_none()

			if question is None:
				abort(422)

			question.delete()
			selection= Question.query.order_by(Question.id).all()
			current_questions = paginate_questions(request, selection)

			return jsonify({
				'success':True,
				'id': question.id,
				'questions': current_questions,
				'total_questions': len(Question.query.all())
			})

		except:
			abort(422)


	@app.route('/questions', methods=['POST'])
	def create_questions():
		'''Add new question by taking data from creation form'''

		try:
			question = request.json['question']
			answer = request.json['answer']
			difficulty = request.json['difficulty']
			category = request.json['category']
			new_question = Question(question=question, answer=answer,
			 difficulty=int(difficulty), category=category)

			new_question.insert()

			selection = Question.query.order_by(Question.id).all()
			current_questions = paginate_questions(request, selection)

			return jsonify({
				"created": new_question.id,
				"success": True,
				'questions': current_questions,
				'total_questions': len(Question.query.all())
			})

		except:
			abort(422)

	@app.route('/search', methods=['POST'])
	def search():
		'''Search for question by in word in question title '''
		search = request.json['search']
		if search:
			selection = Question.query.order_by(Question.id).filter(
			Question.question.ilike('%{}%'.format(search))
			)
			current_questions = paginate_questions(request, selection)

			return jsonify({
				"success": True,
				'questions': current_questions,
				'total_questions': len(selection.all()),
				'current_category': "none"
			})

	@app.route('/categories', methods=['GET'])
	def get_category():
		'''return all categories '''

		categories = Category.query.order_by(Category.id).all()
		categories = {category.id: category.type for category in categories}

		if len(categories) == 0:
			abort(404)

		return jsonify({
			'success':True,
			'categories': categories,
			'total_categories': len(Category.query.all())
		})

	@app.route('/categories/<int:category_id>/questions', methods=['POST'])
	def get_questions_by_category(category_id):
		''' takes category_id as parameter and
		return questions with this category type'''
		selection= Question.query.order_by(Question.id).filter(
		Question.category == category_id
		).all()
		current_questions = paginate_questions(request, selection)

		if len(current_questions) == 0:
			abort(404)

		return jsonify({
			'success': True,
			'questions': current_questions,
			'total_questions': len(selection),
			'current_category': Category.query.filter(
			Category.id == category_id
			).one_or_none().type
		})

	@app.route('/quizzes', methods=['POST'])
	def get_quizzes():
		'''Takes category and previous_questionslist from quizzes page
		and return at most 5 questions of this category '''

		data = request.get_json()
		category = data.get('quiz_category')["id"]
		previous_questions = data.get('previous_questions')
		if int(category)==0:
			selection= Question.query.all()
		else:
			selection= Question.query.filter(
			Question.category==int(category)
			).all()
		current_questions = [question.format() for question in selection]
		question= random.choice(current_questions)
		if len(current_questions) == 0:
			abort(404)

		try:
			if len(current_questions) >= 5:
				if (question['id'] in previous_questions
				and len(previous_questions) < 5):
					while question['id'] in previous_questions:
						question= random.choice(current_questions)
			else:
				if (question['id'] in previous_questions
				and len(previous_questions) < len(current_questions)):
					while question['id'] in previous_questions:
						question= random.choice(current_questions)
				else:
					question= random.choice(current_questions)

			return jsonify({
				'previous_questions': previous_questions,
				'quiz_category': category,
				'question':question,
			})

		except:
			abort(404)

	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
			"success": False,
			"error": 404,
			"message": "resource not found"
		}), 404




	@app.errorhandler(422)
	def not_found(error):
		return jsonify({
			"success": False,
			"error": 422,
			"message": "unprocessable"
		}), 422

	@app.errorhandler(400)
	def not_found(error):
		return jsonify({
			"success": False,
			"error": 400,
			"message": "bad request"
		}), 400

	@app.errorhandler(405)
	def not_found(error):
		return jsonify({
			"success": False,
			"error": 405,
			"message": "method not allowed"
		}), 405




		'''
		@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
		'''

		'''
		@TODO: Use the after_request decorator to set Access-Control-Allow
		'''

		'''
		@TODO:
		Create an endpoint to handle GET requests
		for all available categories.
		'''


		'''
		@TODO:
		Create an endpoint to handle GET requests for questions,
		including pagination (every 10 questions).
		This endpoint should return a list of questions,
		number of total questions, current category, categories.

		TEST: At this point, when you start the application
		you should see questions and categories generated,
		ten questions per page and pagination at the bottom of the screen for three pages.
		Clicking on the page numbers should update the questions.
		'''

		'''
		@TODO:
		Create an endpoint to DELETE question using a question ID.

		TEST: When you click the trash icon next to a question, the question will be removed.
		This removal will persist in the database and when you refresh the page.
		'''

		'''
		@TODO:
		Create an endpoint to POST a new question,
		which will require the question and answer text,
		category, and difficulty score.

		TEST: When you submit a question on the "Add" tab,
		the form will clear and the question will appear at the end of the last page
		of the questions list in the "List" tab.
		'''

		'''
		@TODO:
		Create a POST endpoint to get questions based on a search term.
		It should return any questions for whom the search term
		is a substring of the question.

		TEST: Search by any phrase. The questions list will update to include
		only question that include that string within their question.
		Try using the word "title" to start.
		'''

		'''
		@TODO:
		Create a GET endpoint to get questions based on category.

		TEST: In the "List" tab / main screen, clicking on one of the
		categories in the left column will cause only questions of that
		category to be shown.
		'''


		'''
		@TODO:
		Create a POST endpoint to get questions to play the quiz.
		This endpoint should take category and previous question parameters
		and return a random questions within the given category,
		if provided, and that is not one of the previous questions.

		TEST: In the "Play" tab, after a user selects "All" or a category,
		one question at a time is displayed, the user is allowed to answer
		and shown whether they were correct or not.
		'''

		'''
		@TODO:
		Create error handlers for all expected errors
		including 404 and 422.
		'''

	return app
