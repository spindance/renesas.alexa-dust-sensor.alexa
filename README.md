# Renesas.alexa-dust-sensor.alexa
Contains Renesas IoT Sandbox Dust Sensor and Alexa workflow code, Alexa speech assets, and a walkthrough for creating an Alexa skill and integrating it with the Renesas IoT Sandbox.

# Walkthrough
This walkthrough will guide you through the development of an Alexa skill. You will also learn how to integrate the Alexa skill with the Renesas IoT Sandbox. By the end of the walkthrough you will be able to query Alexa, "Alexa, ask Brainy Office, what is the current air quality?" to which Alexa will reply with "The current air quality is X", where X is the most recent air quality measurement.

## Contents
* [Prerequisites](#prerequisites)
* [Creating Alexa Skill](#creating-alexa-skill)
* [Integrating Alexa with Renesas IoT Sandbox](#integrating-alexa-with-renesas-iot-sandbox)
* [Enable and link the Alexa skill](#enable-and-link-the-alexa-skill)
* [Testing the Alexa skill](#testing-the-alexa-skill)
* [Creating the workflows](#creating-the-workflows)
* [The Finish Line](#the-finish-line)

## Prerequisites
* Completion of the [Smart Garage](http://renesas-blog.mediumone.com/smart-garage-monitoring-tutorial/) and [Smart Chef](http://renesas-blog.mediumone.com/renesas-s3a7-fast-iot-prototyping-kit-with-smart-chef-demo-quick-start-guide/) tutorial.
* A Smart Chef project and its activation email from the project.
* An Amazon Developer account (https://developer.amazon.com/)
* An Echo, Echo Dot, Tap, or [Echosim.io](https://www.echosim.io) to use with Alexa.
* A smartphone with the Amazon Alexa app, or the [web based alexa app](http://alexa.amazon.com/spa/index.html).

## Creating Alexa Skill
Log in to your Amazon Developer account at https://developer.amazon.com (Note that this is not the same thing as an AWS account).
Navigate to the **Alexa** tab in the developer account.

![Alexa Tab](/images/alexa_tab.png)

This walkthrough covers the Alexa Skills Kit, so click on the **Get Started** button under **Alexa Skills Kit**.

![Alexa Skills Kit](/images/alexa_skills_kit.png)

Click **Add a New Skill**.

![Add a new skill](/images/add_skill.png)

For this walkthrough we will be creating a skill type with a **Custom Interaction Model**. Refer to the image below for guidance. The **name** of the skill is displayed in the Alexa mobile application. The **invocation name** is the name the user will speak to when requesting information. In our case we want to talk with **Brainy Office**.

![Skill Information](/images/skill_information.png)

On the **Interaction Model** configuration panel, configure the intent schema, custom types, and sample utterances.
* [Intent Schema](/speechAssets/IntentSchema.json) - The intent schema defines the interface between Alexa and alexa request handlers.
* [Custom Slot Types](/speechAssets/CustomTypes.yml) - Specifies the custom types being used by the intent schema. The file is in yaml format for readability and organizational purpose. Refer to the Alexa Skill Configuration UI for the proper way to insert the data.
* [Sample Utterances](/speechAssets/SampleUtterances.yml) - A list of specific examples that help Alexa understand what the user is attempting to do.

After configuration, the interaction model should look like the following:

![Interaction Model](/images/interaction_model.png)

#### Related Useful Links
https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/overviews/understanding-custom-skills  
https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/defining-the-voice-interface

## Integrating Alexa with Renesas IoT Sandbox
This section covers how to integrate the newly created Alexa skill with the Renesas IoT Sandbox. In order to do this we first need to create a stream on the Renesas IoT Sandbox to receive the Alexa requests from Amazon. After we have created a stream, we then need to create an OAuth client that our Alexa skill can link with. This is required to authenticate and authorize our Alexa skill with a particular account and configuration in the Renesas IoT Sandbox. Once this configuration is completed we then need to finish configuring our Alexa skill on Amazon.

### Creating the Alexa Request Stream
Streams are configured by clicking on **Config -> Data Streams** in the Renesas IoT Sandbox. You will likely have several streams already defined. Scroll to the bottom of the list and click **Create New Stream**

![Add data stream](/images/add_data_stream.png)

Name the new stream, **alexa_requests**, and click **Save Data Stream**. All requests sent by the Alexa service will be delivered to this stream.

### Creating the OAuth client
The OAuth client forms the link between our Alexa. This link is between a user's Amazon Alexa account and a particular user account on the Renesas IoT Sandbox. To begin, navigate to **Setup -> Manage OAuth Clients** configuration page in the Renesas IoT Sandbox. Click the **Add New OAuth Client** button.

Name the client something meaningful such as **Alexa OAuth**. The **Additional login message** is displayed to the user on the login page, during the account linking procedure, within the Alexa mobile phone application.

We need to setup permission for Alexa to publish requests to the **alexa_requests** stream configured previously. Click the **plus button** next to permissions and select the **alexa_requests** stream from the drop down. Be sure to check both **Read Permission** and **Write Permission**. At this point your configuration should look like the image below.

![Alexa requests stream](/images/alexa_requests_stream.png)

Click **Save** when you are ready to move on.

### Finishing the Configuration
Now that we have the OAuth client created on the Renesas IoT Sandbox we now have to share the **Client ID** and **Client Secret** with the Alexa skill configuration. Similarly, the Alexa skill configuration needs to share some configuration details with the Renesas IoT Sandbox.

The **Client Id** and **Client Secret** can be found in the **Manage OAuth Clients** configuration of the Renesas IoT Sandbox. See the image below.

![Client Id and Client Secret](/images/client_id_client_secret.png)

Record the **Client Id** and **Client Secret** for the following steps.

Return to the Alexa skill configuration tool and navigate to the **Configuration** panel. For this walkthrough we are going to use the **HTTPS** **Service Endpoint Type**. Select the geographical region that is appropriate for your usage and paste **https://assistant-rna.mediumone.com/alexa_request?stream=alexa_requests** into the text window. The **stream=alexa_requests** portion of the query string should match the name of the stream that was created previously.

![service endpoint type](/images/service_endpoint_type.png)

Next, select **Yes** for the account linking option and enter in the following information:

* Authorization URL - https://auth-rna.mediumone.com/oauth2/authorize
* Client Id - The **Client Id** recorded above, found in the **Manage OAuth Clients** configuration of the Renesas IoT Sandbox
* Domain List - N/A
* Scope - N/A
* Redirect URLs - ***Record these for following steps***. These will need to be added back into the Renesas IoT Sandbox
* Authorization Grant Type - Select **Auth Code Grant**
  * Access Token URI - https://auth-rna.mediumone.com/oauth2/token
  * Client Secret - The **Client Secret** recorded above, found in the **Manage OAuth Clients** configuration of the Renesas IoT Sandbox
  * Client Authentication Scheme - HTTP Basic
* Permissions - All unchecked

![account linking](/images/account_linking.png)

Fill in the Privacy Policy with https://mediumone.com/privacy

![privacy policy](/images/privacy_policy.png)

Now, back to the Renesas IoT Sandbox **Manage OAuth Clients**. Edit the newly created OAuth client from above.

![edit oauth client](/images/edit_oauth_client.png)

Use the **plus button** next to **Redirect URIs** and copy/paste the **Redirect URLs** from the Alexa skill configuration.

![Redirect urls alexa](/images/redirect_urls_alexa.png)

![OAuth client with redirects](/images/oauth_client_with_redirects.png)

Select **Save** in the **Manage OAuth Clients** tool and the Alexa skill **Configuration** tool.

As a final step in the Alexa skill configuration, on the **SSL Certificate** panel select **"My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority"** and click **Save**

![SSL Certificate](/images/ssl_cert.png)

This completes the configuration between Renesas IoT Sandbox and the Alexa skill. We are now ready to start handling requests, but first, let's enable and link our Alexa skill.

#### Related Useful Links
https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/linking-an-alexa-user-with-a-user-in-your-system

## Enable and link the Alexa skill
Using the Alexa mobile app or the web based version available at http://alexa.amazon.com/spa/index.html navigate to the **Skills** panel. 

![Alexa skills](/images/alexa_skills.png)

In the upper left hand corner select **Your Skills**.

![Alexa skills main](/images/alexa_skills_main.png)

The skill we created above should be in the list.

![Your skills](/images/your_skills.png)

If the skill is not listed, return to the Alexa Skill configuration **Test** page and **Enable** the skill.

![Skill enable](/images/skill_enable.png)

In order for the skill to communicate with the Renesas IoT Sandbox it first must be linked to your Renesas IoT Sandbox account. Select the skill then select the **Link Account** option.

![Link account](/images/link_account.png)

Login to the portal using the username and password of the device you received in your *activation email* for the project. For example, the login might be *device* and the password might be *A1g4KY1E90*

![link account login](/images/link_account_login.png)

If everything is successful you should be displayed a screen similar to the following.

![link successful](/images/link_successful.png)

We are now ready to being testing.

## Testing the Alexa skill
Before we start handling Alexa requests let's check to make sure our skill is functioning and requests are being sent to our **alexa_requests** stream. Open the **Test** panel in the Alexa skill configuration tool. Scroll to the bottom and enter in the utterance of "What is the current air quality?". Click **Ask Renesas Alexa Demo** to send the request. The **Service Request** panel displays the JSON document that is posted to the https://assistant-rna.mediumone.com/alexa_request endpoint. The **Service Response** in this case is "There was an error calling the remote endpoint, which returned HTTP 503 : Service Unavailable". This is ok for right now because the Renesas IoT Sandbox is not handling the alexa requests yet.

![Test1](/images/test_1.png)

Return to the Renesas IoT Sandbox and view the **alexa_requests** data stream.

![view alexa request stream](/images/view_alexa_request_stream.png)

The data stream should contain the request that was just sent by the Alexa skill **Test** tool.

![alexa request stream data](/images/alexa_request_stream_data.png)

Now, let's move on to handling those Alexa requests by creating some workflows.

## Creating the workflows
Two workflows need to be created to handle the air quality measurements. To make the air quality measurement more friendly to the user we are first going to process the raw pcs/0.01ft^3 value into a qualitative description. Second we are then going to respond to the Alexa requests by returning these qualitative descriptions.

### Qualitative air quality workflow
The raw air quality measurements are published the raw event stream with the identifier **pcs**. To being processing the **raw:pcs** values first enter the **Workflow Studio** in the Renesas IoT Sandbox. Click **Create** to beging creating a workflow. Give the workflow a name such as "Grove Dust Sensor Processing".

From the right hand side of the workflow studio find **Tags & Triggers -> raw -> pcs**. Drag the box onto the screen.

![Raw pcs tag](/images/raw_pcs_tag.png)

If the **pcs** value is not available in the **Tags & Triggers -> raw** selection you may have to enable it from **Config -> Data Streams -> raw** by checking **Active** for the **raw:pcs** tag.

![Raw pcs data stream](/images/raw_pcs_data_stream.png)

Now, find **Modules -> Foundation -> Base Python** and drag it onto the screen.

![Base Python module](/images/base_python.png)

Now, find **Output -> Processed Stream - Single** and drag it onto the screen.

![Processed stream](/images/processed_stream.png)

Connect **raw:pcs** to **in1** of the **Base Python** block. Connect **out1** of the **Base Python** block to **in1** of the **Processed Stream - Single** block. When you are finished the workflow should look similar to the image below.

![Dust sensor workflow](/images/dust_sensor_workflow.png)

Double click the **Base Python** block to begin editing the code. Every time a **pcs** value is published to the **raw** stream the code in this block will run. Copy/paste the code from [grove-dust-processing-workflow.py](/src/grove-dust-processing-workflow.py). Click **Save**

Double click the **Processed Stream - Single**. In the **Tag Name** place the value `qualitative_air_quality`. We will use this processed stream value in the Alexa workflow. Click **Save and Activate**

![Processed stream config](/images/processed_stream_config.png)

### Alexa workflow
We would like Alexa to response to our requests. The way to accomplish this within the Renesas IoT Sandbox is to create a workflow to handle the request and provide a response. Begin by entering the **Workflow Studio** in the Renesas IoT Sandbox. Click **Create** to begin creating a workflow. Give the workflow a name such as "Alexa Request Handler".

From the right hand side of the workflow studio find **Tags & Triggers -> alexa_requests -> request.intent.name**. Drag the box onto the screen.

![Request intent name trigger](/images/request_intent_name.png)

Now, find **Modules -> Foundation -> Base Python** and drag it onto the screen.

![Base Python module](/images/base_python.png)

Connect the **alexa_requests:request.intent.name** block to the **Base Python** block. When you are finished the workflow should look similar to the image below.

![workflow layout](/images/workflow_layout.png)

Double click the **Base Python** block to begin editing the code. Every time an Alexa request is published to the **alexa_requests** stream the code in this block will run. Copy/paste the code from [alexa-workflow.py](/src/alexa-workflow.py). Click **Save and Activate**

#### Related Helpful Links
Debugging help - http://renesas-docs.mediumone.com//?workflowstudio#debugging  
IONode Lib - http://renesas-docs.mediumone.com//?libraries/ionode  
Analytics Lib - http://renesas-docs.mediumone.com//?libraries/analytics  
Built-ins - http://renesas-docs.mediumone.com//?libraries/builtin

## The Finish Line
Return back to the Alexa Skill **Test** tool. Try the question, "What is the current air quality?" again. This time you should get a response similar to the following:
```json
{
  "version": "1.0",
  "response": {
    "outputSpeech": {
      "type": "PlainText",
      "text": "The most recent air quality is Very Good"
    },
    "card": {
      "content": "The most recent air quality is Very Good",
      "title": "Brainy Office",
      "type": "Simple"
    },
    "reprompt": {
      "outputSpeech": {
        "type": "PlainText",
        "text": ""
      }
    },
    "shouldEndSession": true
  },
  "sessionAttributes": {}
}
```
Now, you should be able to ask your Alexa enabled device, "Alexa, ask Brainy Office, what is the current air quality?". The response should be "The most recent air quality is ____".

**Congratulations! You have successfully created an Alexa skill and integrated it with the Renesas IoT Sandbox.**
