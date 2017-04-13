# Pynteractor: the Business Logic tool
This tool is a reimplementation in Python of the fantastic [collectiveidea/interactor](https://github.com/collectiveidea/interactor) Ruby library.

## Rationale

Sometimes - particularly when developping web application - it is hard to reason about what should belong to the application logic (e.g. "Is my current call RESTful?") from the [business logic](https://en.wikipedia.org/wiki/Business_logic) (e.g. "What is the outcome of the current action?").

This library is a dead simple set of tools to help decoupling the two domains. It does nothing really magical, it just helps to extract the business logic, and decompose it in various steps.

Main advantages of this are:

* Facilitate thought about what a code should **do**.
* Provide unit testing out of the box.
* Potential reusability.
* Easy dependency injection.

## How to

### The Interactor

It's a simple, stupid small brick that does one and one thing only.
An asy analogy is to compare the **Interactor** as a function, as it has:

* An input
* A logic
* An output

The only difference is that the interactor is implemented as a class, which allows to split and hide dedicated behaviors required to complete a unique task.

Examples of tasks can be:

* Check the given parameters are ok
* Update a user attributes into database
* Notify your team when an event occurs
* Track the current action

#### Interface

The **Interactor** has a simple interface, as well as a simple environment to play with.


An interactor **must** inherit from the `Interactor` class and **must** implement the `run` method.
It has also a `context` object provided as an instance attribute.


For the following example, let's suppose in our controller, we want to create a new user after a signup form has been sent and completed:

```python
from pynteractor import Interactor


class CheckParameters(Interactor):
    def run(self):
        self._check_email_is_not_taken()
        self._check_password_is_provided()
        
    def _check_email_is_not_taken(self):
        if User.objects.get(email=self.context.user_email):
            self.context.fail(message='User email already taken.')
            
    def _check_password_is_provided(self):
        if not self.context.password:
            self.context.fail(message='Please, provide a password')

```

Which will be used as follow:

```python
def create_user_view(request):
    result = CheckParameters.call(user_email=request.POST['email'], password=request.POST['password'])
    
    if result.success:
        user = User(email=request.POST['email'], password=hash_func(request.POST['password']))
```

Pretty simple, isn't it?

Now, we need to know what is this damn `self.context` object.

### The Context

It is a tool that is in charge of two things:

* Storing data using the dot syntax or the square brackets syntax.
* Interrupting the execution of an interactor and signaling the outcome of the execution (success/failure)

For provide the latter, it implements two methods:
* `stop(**kwargs)`: To signal the interactor no longer needs to be executed. Compared to the function allegory you can picture it as a `return` statement. The provided args will be added to the context right before stopping the execution of the current interactor.
* `fail(**kwargs)`: similar to stop, except it sets the current interactor state to failure.

To know if an interactor execution has succeeded from the outside, you can test two boolean values:
* `success`
* `failure`

Each value is the strict opposite of the other one.

Example:

```python
from pynteractor.context import Context

ctx = Context(name='John Doe')
print(ctx.name) # John Doe
ctx.age = 42
ctx['location'] = 'Unknown'
print(ctx.unroll()) # {'name': 'John Doe', 'age': 42, 'location': 'unknown', 'success': True, 'failure': False}
ctx.fail(reason='Because why not!')
print(ctx.success) # False
print(ctx.failure) # True
print(ctx.reason) # Because why not!
```

### The Organizer

The `Organizer` is an `Interactor` with a difference: its purpose is to execute multiple `Interactor`s. To do so, a class must inherit from the `Organizer` class and provide a `interactors` static attribute, which is a list of reference to uninstanciated `Interactor`s.

Example:

```python
from pynteractor import Organizer

from myproject.update_user import CheckParameters, RegisterUser, SendWelcomeEmail

class Signup(Organizer):
    interactors = [CheckParameters, RegisterUser, SendWelcomeEmail]
```

In the controller/view:

```python
def register_user(request):
    result = Signup.call(user_email=request.POST['email'], user_password=request.POST['password'])
    
    if result.success == True:
        # `result` is the context returned by the Organizer,
        # `user` is the created used entity created by `RegisterUser`
        return HttpResponse(serialize(result.user), content_type="application/json")
    else:
        return  HttpResponseBadRequest()

```