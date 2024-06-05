from setuptools import setup, find_packages

setup(
    name='learn-scheduler',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'openai',
        'python-dotenv',
        'pytest'
    ],
    entry_points={
        'console_scripts': [
            'calendar_fetch=calendar_fetch:main',
            'create_event=create_event:main',
            'feed_llm=feed_llm:main'
        ],
    },
)