from web3 import Web3,HTTPProvider
from flask import Flask,render_template,redirect,request,jsonify,session
import json
import bcrypt
from werkzeug.utils import secure_filename
import os
import hashlib

userManagementArtifactPath="../build/contracts/userManagement.json"
InsuranceClaimArtifactPath="../build/contracts/InsuranceClaim.json"
blockchainServer="http://127.0.0.1:7545"

def connectWithContract(wallet,artifact=userManagementArtifactPath):
    web3=Web3(HTTPProvider(blockchainServer)) # it is connecting with server
    print('Connected with Blockchain Server')

    if (wallet==0):
        web3.eth.defaultAccount=web3.eth.accounts[0]
    else:
        web3.eth.defaultAccount=wallet
    print('Wallet Selected')

    with open(artifact) as f:
        artifact_json=json.load(f)
        contract_abi=artifact_json['abi']
        contract_address=artifact_json['networks']['5777']['address']
    
    contract=web3.eth.contract(abi=contract_abi,address=contract_address)
    print('Contract Selected')
    return contract,web3

app=Flask(__name__)
app.secret_key="M@keskilled0"

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure base upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/signup')
def signupPage():
    return render_template('signup.html')

@app.route('/register',methods=['POST']) # page (1 Route), page (2 Route)
def register():
    role=request.form['role']
    wallet=request.form['address']
    username=request.form['username']
    email=request.form['email']
    password=request.form['password']
    confirmPassword=request.form['confirmPassword']

    if(password!=confirmPassword):
        return render_template('signup.html',message='passwords not matched, try again')
    
    contract,web3=connectWithContract(wallet) # UserManagement
    try:
        tx_hash=contract.functions.userSignUp(wallet,username,password,role,email).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        print('Transaction Successful')
        return render_template('signup.html',message='Signup Successful')
    except:
        return render_template('signup.html',message='there is problem in creating account')

@app.route('/loginForm',methods=['POST'])
def loginForm():
    username=request.form['username']
    password=request.form['password']

    contract,web3=connectWithContract(0)
    try:
        result=contract.functions.userLogin(username,password).call()
        print(result)
        if result==True:
            response=contract.functions.viewUserByUsername(username).call()
            print (response)
            session['userwallet']=response[0]
            session['username']=response[1]
            session['userrole']=response[3]
            session['useremail']=response[-2]
            if session['userrole']=='user':
                return redirect('/userDashboard')
            elif session['userrole']=='police':
                return redirect('/policeHome')
            elif session['userrole']=='hospital':
                return redirect('/hospitalDashboard')
            return render_template('login.html',message='success')
        else:
            return render_template('login.html',message='Invalid credentials')
    except Exception as e:
        print(e)
        return render_template('login.html',message='Invalid details of username')

@app.route('/userDashboard')
def userDashboard():
    return render_template('Lifeinsurance.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/upload/user-details',methods=['POST'])
def uploadUserDetails():
    wallet=session['userwallet']
    insuranceType=request.form['insurance_type']
    policyId=request.form['policy_id']
    adharNumber=request.form['aadhaar_number']
    phoneNumber=request.form['phone_number']

    contract,web3=connectWithContract(wallet,InsuranceClaimArtifactPath)
    print('Contract Connected')
    try:
        tx_hash=contract.functions.addUserDetails(wallet,insuranceType,policyId,adharNumber,phoneNumber).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('Lifeinsurance.html',message='User Details Added Successfully')
    except:
        return render_template('Lifeinsurance.html',message='Problem adding details')

@app.route('/upload/nominee-details',methods=['POST'])
def uploadNomineeDetails():
    wallet=session['userwallet']
    nomineeName=request.form['nominee_name']
    nomineeAdharNumber=request.form['nominee_aadhaar']
    nomineePhoneNumber=request.form['nominee_phone']

    contract,web3=connectWithContract(wallet,InsuranceClaimArtifactPath)
    print('Contract Connected')
    try:
        tx_hash=contract.functions.addNomineeDetails(wallet,nomineeName,nomineeAdharNumber,nomineePhoneNumber).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('Lifeinsurance.html',message1='Nominee Details Added')
    except:
        return render_template('Lifeinsurance.html',message1='Problem adding Nominee Details')

@app.route('/upload/bank-details',methods=['POST'])
def uploadBankDetails():
    wallet=session['userwallet']
    bankName=request.form['bank_name']
    accountNumber=request.form['account_number']
    ifscCode=request.form['ifsc_code']

    contract,web3=connectWithContract(wallet,InsuranceClaimArtifactPath)
    print('Contract Connected')

    try:
        tx_hash=contract.functions.addBankDetails(wallet,bankName,accountNumber,ifscCode).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('Lifeinsurance.html',message2='Bank Details Added')
    except:
        return render_template('Lifeinsurance.html',message2='Problem adding Bank Details')


@app.route('/upload/certificate-upload',methods=['POST'])
def uploadCertificateDetails():
    policy_photo = request.files['policy_photo']
    reports = request.files['reports']

    # Check if the files have names
    if policy_photo.filename == '' or reports.filename == '':
        return render_template('Lifeinsurance.html', message3="No file selected for one or more fields.")

    # Create subdirectory path dynamically
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['userrole'])
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)  # Create folder if it doesn't exist

    # Secure and save files
    policy_photo_filename = secure_filename(policy_photo.filename)
    reports_filename = secure_filename(reports.filename)

    policy_photo_path = os.path.join(user_folder, policy_photo_filename)
    reports_path = os.path.join(user_folder, reports_filename)

    # Save files locally or to the specified directory
    policy_photo.save(policy_photo_path)
    reports.save(reports_path)

    # Generate hashes for the files
    policy_photo.seek(0)  # Reset the file pointer
    reports.seek(0)       # Reset the file pointer
    policy_photo_hash = hashlib.sha256(policy_photo.read()).hexdigest()
    reports_hash = hashlib.sha256(reports.read()).hexdigest()

    print(f"Policy photo hash: {policy_photo_hash}")
    print(f"Reports hash: {reports_hash}")
    wallet=session['userwallet']

    contract,web3=connectWithContract(wallet,InsuranceClaimArtifactPath)
    print('Contract Connected')

    try:
        tx_hash=contract.functions.addCertificateDetails(wallet,policy_photo_path,policy_photo_hash,reports_path,reports_hash).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)

        return render_template('Lifeinsurance.html', message3="Uploaded Files successfully.")
    except:
        return render_template('Lifeinsurance.html', message3="Problem uploading files.")

@app.route('/admin')
def adminPage():
    return render_template('adminlogin.html')

@app.route('/adminLoginForm',methods=['POST'])
def adminLoginForm():
    username=request.form['username']
    password=request.form['password']
    
    contract,web3=connectWithContract(0)
    print('Contract Connected')

    result=contract.functions.validateAdmin(username,password).call()
    if result==True:
        session['userrole']='admin'
        return redirect('/adminDashboard')
    else:
        return render_template('adminlogin.html',message='Invalid credentials')

@app.route('/adminDashboard')
def adminDashboard():
    contract,web3=connectWithContract(0,InsuranceClaimArtifactPath)
    response=contract.functions.viewAllUserDetails().call()
    print(response)
    data=[]
    for i in range(len(response)):
        dummy=[]
        dummy.append(response[i][0])
        dummy.append(response[i][1])
        dummy.append(response[i][2])
        dummy.append(response[i][3])
        dummy.append(response[i][4])
        data.append(dummy)
    print(data)
    return render_template('adminhome.html',data=data,l=len(data))

@app.route('/viewApplicationDetails/<wallet>')
def viewApplicationDetails(wallet):
    contract,web3=connectWithContract(0,InsuranceClaimArtifactPath)
    try:
        userdetails=contract.functions.viewUserDetailsByWallet(wallet).call()
        print(userdetails)
    except:
        userdetails=['NA','NA','NA','NA','NA','NA']
        print('User Details Empty')
    
    try:
        nomineedetails=contract.functions.viewNomineeDetailsByWallet(wallet).call()
        print(nomineedetails)
    except:
        nomineedetails=['NA','NA','NA','NA','NA']
        print('Nominee Details Empty')

    try:
        bankdetails=contract.functions.viewBankDetailsByWallet(wallet).call()
        print(bankdetails)
    except:
        bankdetails=['NA','NA','NA','NA','NA']
        print('Bank Details Empty')
    
    try:
        certificatedetails=contract.functions.viewCertificateDetailsByWallet(wallet).call()
        print(certificatedetails)
    except:
        certificatedetails=['NA','NA','NA','NA','NA']
        print('CertificateDetailsEmpty')

    return render_template('admindashboard.html',userdetails=userdetails,nomineedetails=nomineedetails,bankdetails=bankdetails,certificatedetails=certificatedetails)

@app.route('/policeHome')
def policeHome():
    return render_template('policehome.html')

@app.route('/upload/police-details',methods=["GET","POST"])
def uploadPoliceDetails():
    if request.method == "GET":
        contract,web3=connectWithContract(0,InsuranceClaimArtifactPath)
        response=contract.functions.viewAllUserDetails().call()
        policyIds=[]
        for i in response:
            policyIds.append(i[2])
        print(policyIds)
        return render_template('police_dashboard.html',policy_ids=policyIds)

    if request.method == "POST":
        policy_id = request.form['policy_id']
        full_name = request.form['full_name']
        contact_info = request.form['contact_info']
        photo = request.files['user_photo']

        if not policy_id or not full_name or not contact_info or not photo:
            return render_template('police_dashboard.html', error="All fields are required."), 400

        # Secure and save the uploaded photo in the 'hospital' folder inside the UPLOAD_FOLDER
        police_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['userrole'])
        # Create the 'hospital' folder if it doesn't exist
        if not os.path.exists(police_folder):
            os.makedirs(police_folder)
        
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(police_folder, filename)  # Save inside 'hospital' folder
        photo.save(photo_path)

        # Assuming we want to hash the photo for verification later
        photo.seek(0)  # Reset the file pointer
        photo_hash = hashlib.sha256(photo.read()).hexdigest()
        wallet=session['userwallet']
        print(wallet)
        contract,web3=connectWithContract(wallet,InsuranceClaimArtifactPath)
        try:
            tx_hash=contract.functions.addPoliceDetails(wallet,policy_id,full_name,contact_info,photo_path,photo_hash).transact()
            web3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_hash)
            return render_template('police_dashboard.html',message="Uploaded Files successfully.")
        except:
            return render_template('police_dashboard.html',message="Problem uploading files.")

@app.route('/police/reports')
def viewPoliceReports():
    contract,web3=connectWithContract(0,InsuranceClaimArtifactPath)
    reports = contract.functions.viewAllPoliceDetails().call()
    print(reports)
    return render_template('policereports.html',reports=reports)



if __name__=="__main__":
    app.run(host='0.0.0.0',port=9000,debug=True)








